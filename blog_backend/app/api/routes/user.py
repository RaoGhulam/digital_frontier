from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, login_rate_limit
from app.db.database import get_db

from app.models.user import User

from app.schemas.user import (
    DeleteUserResponse,
    LoginRequest,
    LoginResponse,
    UserCreate,
    UserRead,
)

from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/signup",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    description="Register a new user account",
)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    return user_service.register_user(
        db,
        user_in,
    )


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    description="Authenticate user and return access token",
    dependencies=[Depends(login_rate_limit)],
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    token = user_service.login_user(
        db,
        payload.email,
        payload.password,
    )

    return LoginResponse(
        access_token=token
    )



@router.delete(
    "/account",
    response_model=DeleteUserResponse,
    status_code=status.HTTP_200_OK,
    description="Delete the currently authenticated user account",
)
def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service.delete_user_account(
        db,
        current_user,
    )

    return DeleteUserResponse(
        message="Account deleted successfully"
    )


@router.get("/verify-email")
def verify_email(
    token: str,
    db: Session = Depends(get_db),
):
    message = user_service.verify_user_email(
        db,
        token,
    )

    return {
        "message": message,
    }