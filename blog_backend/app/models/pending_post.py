import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, ForeignKey, String, Text, TIMESTAMP, text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.core.enums import PostStatus


def postgres_enum(enum_class, name):
    return Enum(
        enum_class,
        name=name,
        values_callable=lambda enum_cls: [item.value for item in enum_cls],
        validate_strings=True,
    )


class PendingPost(Base):
    __tablename__ = "pending_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    author_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=True, index=True)

    content = Column(Text, nullable=False)

    category = Column(String(50), nullable=False, index=True)

    status = Column(
        postgres_enum(PostStatus, "post_status_enum"),
        nullable=False,
        default=PostStatus.PENDING,
        server_default=PostStatus.PENDING.value,
    )

    reviewed_by = Column(
        UUID(as_uuid=True),
        ForeignKey("admins.id", ondelete="SET NULL"),
        nullable=True,
    )

    reviewed_at = Column(TIMESTAMP, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    # optional: becomes real publish time after approval
    published_at = Column(TIMESTAMP, nullable=True)

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.now(timezone.utc),
    )

    author = relationship("User", backref="pending_posts")
    reviewer = relationship("Admin", backref="reviewed_posts")