from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_optional_current_user
from app.db.database import get_db
from app.models.user import User

from app.schemas.post import (
    CreatePostResponse,
    DeletePostResponse,
    PostCreate,
    PostDetailResponse,
    PostListResponse,
)

from app.services.post_service import (
    create_pending_post,
    delete_post_by_slug,
    get_post_detail,
    get_posts,
    get_user_posts,
)

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get(
    "",
    response_model=PostListResponse,
    description="Retrieve a paginated list of posts with optional filtering and sorting",
)
def list_posts(
    category: str = Query(default="all"),
    sort_by: str = Query(default="latest"),
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
):
    return get_posts(
        db=db,
        category=category,
        sort_by=sort_by,
        page=page,
    )


@router.post(
    "/create",
    response_model=CreatePostResponse,
    description="Create a new post and submit it for review",
)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    pending_post = create_pending_post(
        db,
        current_user,
        data,
    )

    return {
        "message": "Post submitted for review",
        "post": pending_post,
    }


@router.get(
    "/my-posts",
    response_model=PostListResponse,
    description="Retrieve posts created by the current user with filtering options",
)
def my_posts(
    is_published: str = Query(
        "all",
        pattern="^(all|published|unpublished)$",
    ),
    sort_by: str = Query(
        "latest",
        pattern="^(latest|oldest)$",
    ),
    page: int = Query(1, ge=1),
    per_page: int = Query(9, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_user_posts(
        db=db,
        user_id=current_user.id,
        is_published=is_published,
        sort_by=sort_by,
        page=page,
        per_page=per_page,
    )


@router.get(
    "/{slug}",
    response_model=PostDetailResponse,
    description="Retrieve detailed information of a single post by slug",
)
def read_post(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    return get_post_detail(
        db,
        slug,
        current_user,
    )


@router.delete(
    "/{slug}",
    response_model=DeletePostResponse,
    description="Delete a post by slug if the user has permission",
)
def delete_post(
    slug: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    post = delete_post_by_slug(
        db,
        slug,
        current_user.id,
    )

    return {
        "message": "Post deleted successfully",
        "deleted_post_id": post.id,
    }