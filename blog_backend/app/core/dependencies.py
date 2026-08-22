from fastapi import Depends, Cookie, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db

from app.models.admin import Admin
from app.models.user import User

from app.core.exceptions import (
    InvalidTokenError,
    UserNotFoundError,
    UserDeletedError,
    AdminNotFoundError,
    AdminInactiveError,
    SuperAdminRequiredError,
    LoginRateLimitExceededError,
)

from app.core.redis import redis_client


# Swagger/OpenAPI compatible Bearer authentication
bearer_scheme = HTTPBearer(auto_error=False)


def get_access_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    access_token: str | None = Cookie(None),
):
    """
    Get JWT token from:

    1. Authorization header:
       Authorization: Bearer <token>

    2. Cookie:
       access_token=<token>

    Bearer token has priority.
    """

    if credentials:
        return credentials.credentials

    if access_token:
        return access_token

    raise InvalidTokenError()


def decode_token(token: str):
    """
    Decode and validate JWT token.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        subject = payload.get("sub")

        if not subject:
            raise InvalidTokenError()

        return subject

    except JWTError:
        raise InvalidTokenError()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(get_access_token),
):
    """
    Required user authentication.
    """

    user_id = decode_token(token)

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise UserNotFoundError()

    if user.status == "deleted":
        raise UserDeletedError()

    return user


def get_optional_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    access_token: str | None = Cookie(None),
):
    """
    Optional authentication.

    Returns:
    - User object if valid token exists
    - None if no token or invalid token
    """

    token = None

    if credentials:
        token = credentials.credentials

    elif access_token:
        token = access_token

    if not token:
        return None

    try:
        user_id = decode_token(token)

    except InvalidTokenError:
        return None


    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return None

    if user.status == "deleted":
        return None

    return user


def get_current_admin(
    db: Session = Depends(get_db),
    token: str = Depends(get_access_token),
):
    """
    Required admin authentication.
    Only superadmin allowed.
    """

    admin_id = decode_token(token)

    admin = db.query(Admin).filter(
        Admin.id == admin_id
    ).first()

    if not admin:
        raise AdminNotFoundError()

    if not admin.is_active:
        raise AdminInactiveError()

    if admin.role != "superadmin":
        raise SuperAdminRequiredError()

    return admin

# ---------------------------
# Rate Limiting
# ---------------------------

MAX_ATTEMPTS = 5
WINDOW_SECONDS = 60

def login_rate_limit(
    request: Request,
):
    """
    Required login rate limiting.
    Limits login attempts per client IP.
    """

    client_ip = request.client.host

    key = f"rate_limit:login:{client_ip}"

    attempts = redis_client.incr(key)

    if attempts == 1:
        redis_client.expire(key, WINDOW_SECONDS)

    if attempts > MAX_ATTEMPTS:
        raise LoginRateLimitExceededError()

    return True
