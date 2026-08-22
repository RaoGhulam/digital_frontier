import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    """Payload received from the sign-up form."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    username: str = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)


class UserRead(BaseModel):
    """Safe representation of a user returned to clients (no password hash)."""

    id: uuid.UUID
    email: EmailStr
    username: Optional[str] = None
    phone_number: Optional[str] = None
    is_verified: bool
    status: str
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DeleteUserResponse(BaseModel):
    message: str