from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db

from app.schemas.post import PostListResponse
from app.schemas.reaction import ReactionRequest, ReactionResponse

from app.services.reaction_service import (
    get_liked_posts_by_user,
    set_reaction,
)


router = APIRouter(prefix="/reactions", tags=["Reactions"])

@router.get(
    "/liked-posts",
    response_model=PostListResponse,
    description="Get posts liked by the current user",
)
def liked_posts(
    page: int = Query(1, ge=1),
    per_page: int = Query(9, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_liked_posts_by_user(
        db=db,
        user_id=current_user.id,
        page=page,
        per_page=per_page,
    )


@router.post(
    "/reaction",
    response_model=ReactionResponse,
    description="Add or update a reaction on a post",
)
def react_to_post(
    payload: ReactionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return set_reaction(
        db=db,
        post_id=payload.post_id,
        user_id=current_user.id,
        reaction=payload.reaction,
    )