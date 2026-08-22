from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db

from app.schemas.comment import (
    CommentCreate,
    CommentResponse,
    DeleteCommentResponse,
    ReplyCreate,
)
from app.schemas.post import PostListResponse

from app.services.comment_service import (
    add_comment,
    delete_comment_by_user,
    get_commented_posts_by_user,
    reply_to_comment,
)

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get(
    "/commented-posts",
    response_model=PostListResponse,
    description="Get posts that the current user has commented on",
)
def commented_posts(
    page: int = Query(1, ge=1),
    per_page: int = Query(9, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_commented_posts_by_user(
        db=db,
        user_id=current_user.id,
        page=page,
        per_page=per_page,
    )


@router.post(
    "/",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
    description="Add a new comment to a post",
)
def comment_on_post(
    request: CommentCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return add_comment(
        db=db,
        post_id=request.post_id,
        user_id=current_user.id,
        content=request.content,
    )


@router.post(
    "/{comment_id}/reply",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
    description="Reply to an existing comment",
)
def reply_comment(
    comment_id: UUID,
    request: ReplyCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return reply_to_comment(
        db=db,
        comment_id=comment_id,
        user_id=current_user.id,
        content=request.content,
    )


@router.delete(
    "/{comment_id}",
    response_model=DeleteCommentResponse,
    status_code=status.HTTP_200_OK,
    description="Delete a comment owned by the current user",
)
def delete_comment(
    comment_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    delete_comment_by_user(
        db=db,
        comment_id=comment_id,
        user_id=current_user.id,
    )

    return {
        "success": True,
        "message": "Comment deleted successfully",
    }