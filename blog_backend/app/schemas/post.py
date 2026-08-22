from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.enums import ReactionType


class PostListItem(BaseModel):
    id: UUID
    title: str
    slug: str
    category: str
    author_name: str
    published_at: datetime | None
    created_at: datetime

    likes: int
    dislikes: int
    comments: int

    class Config:
        from_attributes = True


class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int


class PostListResponse(BaseModel):
    posts: list[PostListItem]
    pagination: PaginationMeta


class UserSummary(BaseModel):
    id: UUID
    username: str | None

    class Config:
        from_attributes = True


class PostAuthor(UserSummary):
    pass


class PostReactions(BaseModel):
    likes: int
    dislikes: int


class CommentOut(BaseModel):
    id: UUID
    post_id: UUID
    content: str
    created_at: datetime

    user: UserSummary
    replies: list["CommentOut"] = Field(default_factory=list)

    class Config:
        from_attributes = True


CommentOut.model_rebuild()


class PostDetailResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    category: str
    content: str

    published_at: datetime | None
    created_at: datetime
    updated_at: datetime | None

    author: PostAuthor
    reactions: PostReactions
    user_reaction: ReactionType | None = None

    comment_count: int
    comments: list[CommentOut]

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    slug: str = Field(min_length=3, max_length=255)
    content: str
    category: str


class PendingPostResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    category: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class CreatePostResponse(BaseModel):
    message: str
    post: PendingPostResponse


class DeletePostResponse(BaseModel):
    message: str
    deleted_post_id: UUID