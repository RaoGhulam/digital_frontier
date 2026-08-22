from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.reaction import ReactionType


class ReactionRequest(BaseModel):
    post_id: UUID
    reaction: Optional[ReactionType]  # LIKE / DISLIKE / None


class ReactionResponse(BaseModel):
    success: bool
    message: str
    post_id: UUID
    reaction: Optional[ReactionType]