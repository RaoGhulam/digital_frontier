import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password

from app.models.user import User

from app.schemas.user import UserCreate

from app.core.exceptions import (
    UserAlreadyExistsError,
    UserInactiveError,
    AuthenticationError,
    EmailVerificationTokenInvalid,
    UserNotFoundError,
    EmailNotVerifiedError,
)

from app.core.enums import UserStatus

from app.services.email_verification_service import create_verification_token
from app.core.queue import email_queue
from app.tasks.email_tasks import send_verification_email
from app.core.redis import redis_client


# ---------------------------
# Sign Up
# ---------------------------

def register_user(
    db: Session,
    user_in: UserCreate,
) -> User:

    existing_user = (
        db.query(User)
        .filter(User.email == user_in.email)
        .first()
    )

    if existing_user:
        if existing_user.status == UserStatus.DELETED:

            existing_user.status = UserStatus.ACTIVE
            existing_user.password_hash = hash_password(
                user_in.password
            )
            existing_user.username = user_in.username
            existing_user.phone_number = user_in.phone_number
            existing_user.is_verified = False
            existing_user.updated_at = datetime.now(timezone.utc)

            commit_transaction(db)
            db.refresh(existing_user)

            # Generate new verification token
            token = create_verification_token(
                existing_user.id
            )

            verification_url = (
                f"{settings.FRONTEND_URL}/verify-email"
                f"?token={token}"
            )

            email_queue.enqueue(
                send_verification_email,
                existing_user.email,
                verification_url,
            )

            return existing_user

        raise UserAlreadyExistsError(
            "Email already registered."
        )

    new_user = User(
        id=uuid.uuid4(),
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        username=user_in.username,
        phone_number=user_in.phone_number,
        status=UserStatus.ACTIVE,
        is_verified=False,
    )

    db.add(new_user)

    try:
        commit_transaction(db)
    except IntegrityError:
        db.rollback()
        raise UserAlreadyExistsError(
            "Email already registered."
        )

    db.refresh(new_user)

    token = create_verification_token(
        new_user.id
    )

    verification_url = (
        f"{settings.FRONTEND_URL}/verify-email"
        f"?token={token}"
    )

    email_queue.enqueue(
        send_verification_email,
        new_user.email,
        verification_url,
    )

    return new_user


# ---------------------------
# Verification
# ---------------------------

def verify_user_email(
    db: Session,
    token: str,
) -> str:
    key = f"email_verification:{token}"

    # 1. Look up token in Redis
    user_id = redis_client.get(key)

    if not user_id:
        raise EmailVerificationTokenInvalid

    # 2. Find user in PostgreSQL
    user = (
        db.query(User)
        .filter(User.id == uuid.UUID(user_id))
        .first()
    )

    if not user:
        # Token is no longer useful
        redis_client.delete(key)

        raise UserNotFoundError

    # 3. Already verified
    if user.is_verified:
        redis_client.delete(key)

        return "Email is already verified."

    # 4. Mark email as verified
    user.is_verified = True

    commit_transaction(db)

    # 5. Delete token so it cannot be reused
    redis_client.delete(key)

    return "Email verified successfully."



# ---------------------------
# Authentication
# ---------------------------

def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User:
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        raise AuthenticationError()

    if user.status != UserStatus.ACTIVE:
        raise UserInactiveError()

    if not verify_password(password, user.password_hash):
        raise AuthenticationError()

    if not user.is_verified:
        raise EmailNotVerifiedError()

    return user



def login_user(db: Session, email: str, password: str) -> str:
    user = authenticate_user(db, email, password)

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email
        },
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    user.last_login_at = datetime.now(timezone.utc)
    commit_transaction(db)

    return access_token


# ---------------------------
# Delete Account
# ---------------------------

def delete_user_account(db: Session, user: User) -> User:
    user.status = UserStatus.DELETED
    user.updated_at = datetime.now(timezone.utc)

    commit_transaction(db)

    db.refresh(user)

    return user

# ---------------------------
# Helper
# ---------------------------
def commit_transaction(db: Session):
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise