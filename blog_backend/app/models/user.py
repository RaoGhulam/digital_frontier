import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, String, TIMESTAMP, text, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base
from app.core.enums import UserStatus


def postgres_enum(enum_class, name):
    return Enum(
        enum_class,
        name=name,
        values_callable=lambda enum_cls: [item.value for item in enum_cls],
        validate_strings=True,
    )


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    username = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    is_verified = Column(Boolean, server_default=text("false"), default=False)
    status = Column(
        postgres_enum(UserStatus, "user_status_enum"),
        nullable=False,
        default=UserStatus.ACTIVE,
        server_default=UserStatus.ACTIVE.value,
    )
    last_login_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.now(timezone.utc),
    )
