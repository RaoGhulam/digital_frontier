from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, verify_password

from app.models.admin import Admin
from app.models.pending_post import PendingPost
from app.models.post import Post

from app.core.exceptions import (
    AdminNotFoundError,
    InvalidCredentialsError,
    AdminInactiveError,
    AdminPermissionError,
    PendingPostNotFoundError,
    InvalidModerationActionError,
)

from app.core.enums import (
    AdminRole,
    PostStatus,
    ModerationAction,
)

# ---------------------------
# Authentication
# ---------------------------

def admin_login(db: Session, email: str, password: str) -> str:
    admin = db.query(Admin).filter(Admin.email == email).first()

    if not admin:
        raise AdminNotFoundError("Admin not found")

    if not verify_password(password, admin.password_hash):
        raise InvalidCredentialsError("Invalid password")

    if not admin.is_active:
        raise AdminInactiveError("Admin account is inactive")

    if admin.role != AdminRole.SUPERADMIN:
        raise AdminPermissionError("Insufficient permissions")

    admin.last_login_at = datetime.now(timezone.utc)
    commit_transaction(db)

    return create_access_token(
        data={
            "sub": str(admin.id),
            "role": admin.role.value,
            "email": admin.email,
        },
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )


def get_all_pending_posts(db: Session):
    return (
        db.query(PendingPost)
        .filter(PendingPost.status == PostStatus.PENDING)
        .order_by(PendingPost.created_at.desc())
        .all()
    )


# ---------------------------
# Moderation
# ---------------------------

def moderate_pending_post(
    db: Session,
    pending_post_id: int,
    admin_id: int,
    action: ModerationAction,
    rejection_reason: str | None = None
) -> dict:

    pending_post = (
        db.query(PendingPost)
        .filter(PendingPost.id == pending_post_id)
        .first()
    )

    if not pending_post:
        raise PendingPostNotFoundError(
            f"Pending post {pending_post_id} not found"
        )

    if action == ModerationAction.APPROVE:

        new_post = Post(
            author_id=pending_post.author_id,
            title=pending_post.title,
            slug=pending_post.slug,
            content=pending_post.content,
            category=pending_post.category,
            status=PostStatus.PUBLISHED,
            published_at=datetime.now(timezone.utc),
        )

        db.add(new_post)
        db.delete(pending_post)
        commit_transaction(db)

        return {
            "success": True,
            "message": "Post approved and published",
            "post_id": new_post.id
        }

    if action == ModerationAction.REJECT:

        pending_post.status = PostStatus.REJECTED
        pending_post.rejection_reason = rejection_reason
        pending_post.reviewed_by = admin_id
        pending_post.reviewed_at = datetime.now(timezone.utc)

        db.delete(pending_post)
        commit_transaction(db)

        return {
            "success": True,
            "message": "Post rejected and removed"
        }

    raise InvalidModerationActionError(
        f"Invalid action: {action}"
    )

# ---------------------------
# Helper
# ---------------------------
def commit_transaction(db: Session):
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise