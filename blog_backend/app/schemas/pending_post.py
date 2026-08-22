from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel


class ModeratePostRequest(BaseModel):
    action: Literal["approve", "reject"]
    rejection_reason: str | None = None


class ModeratePostResponse(BaseModel):
    success: bool
    message: str
    post_id: UUID | None = None