from uuid import UUID

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.core.dependencies import get_current_admin, login_rate_limit
from app.db.database import get_db

from app.schemas.admin import AdminLogin, AdminToken
from app.schemas.pending_post import ModeratePostRequest, ModeratePostResponse

from app.services.admin_service import (
    admin_login,
    get_all_pending_posts,
    moderate_pending_post,
)

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post(
    "/login",
    response_model=AdminToken,
    description="Authenticate admin and return access token",
    dependencies=[Depends(login_rate_limit)],
)
def login(
    payload: AdminLogin,
    db: Session = Depends(get_db),
):
    token = admin_login(
        db,
        payload.email,
        payload.password,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }



@router.get(
    "/pending-posts",
    description="Fetches all posts that are pending for approval.",
)
def fetch_pending_posts(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    pending_posts = get_all_pending_posts(db)

    return {
        "status": "success",
        "count": len(pending_posts),
        "data": pending_posts,
    }


@router.post(
    "/moderate-post/{pending_post_id}",
    response_model=ModeratePostResponse,
    description="Moderate a pending post by approving or rejecting it",
)
def moderate_post(
    pending_post_id: UUID,
    payload: ModeratePostRequest,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    return moderate_pending_post(
        db=db,
        pending_post_id=pending_post_id,
        admin_id=current_admin.id,
        action=payload.action,
        rejection_reason=payload.rejection_reason,
    )