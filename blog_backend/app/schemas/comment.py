from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    post_id: UUID
    content: str = Field(..., min_length=1, max_length=5000)


class ReplyCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)


class CommentUserResponse(BaseModel):
    id: UUID
    username: str | None

    class Config:
        from_attributes = True


class CommentResponse(BaseModel):
    id: UUID
    post_id: UUID
    content: str
    created_at: datetime

    user: CommentUserResponse
    replies: list["CommentResponse"] = Field(default_factory=list)

    class Config:
        from_attributes = True


CommentResponse.model_rebuild()


class DeleteCommentResponse(BaseModel):
    success: bool
    message: str