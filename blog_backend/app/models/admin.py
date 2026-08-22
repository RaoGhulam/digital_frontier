import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, String, TIMESTAMP, text, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base
from app.core.enums import AdminRole


def postgres_enum(enum_class, name):
    return Enum(
        enum_class,
        name=name,
        values_callable=lambda enum_cls: [item.value for item in enum_cls],
        validate_strings=True,
    )


class Admin(Base):
    __tablename__ = "admins"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String(150), nullable=True)
    role = Column(
        postgres_enum(AdminRole, "admin_role_enum"),
        nullable=False,
        default=AdminRole.MODERATOR,
        server_default=AdminRole.MODERATOR.value,
    )
    is_active = Column(Boolean, server_default=text("true"), default=True)
    last_login_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.now(timezone.utc),
    )