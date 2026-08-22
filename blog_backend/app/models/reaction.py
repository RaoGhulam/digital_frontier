import uuid

from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    TIMESTAMP,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.core.enums import ReactionType


def postgres_enum(enum_class, name):
    return Enum(
        enum_class,
        name=name,
        values_callable=lambda enum_cls: [item.value for item in enum_cls],
        validate_strings=True,
    )


class PostReaction(Base):
    __tablename__ = "post_reactions"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "post_id",
            name="uq_user_post_reaction"
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    post_id = Column(
        UUID(as_uuid=True),
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    reaction = Column(
        postgres_enum(ReactionType, "reaction_type_enum"),
        nullable=False,
    )

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    user = relationship(
        "User",
        backref="post_reactions"
    )

    post = relationship(
        "Post",
        back_populates="reactions"
    )