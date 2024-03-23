from fastapi import APIRouter, Depends, HTTPException
import starlette.status as status
from datetime import timedelta
from typing import Annotated

from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from src.auth.schemas import CreateUserRequest

from src.auth import service
from src.auth.schemas import Token, UserLoginRequest
from src.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(
    create_user_request: CreateUserRequest, db: Session = Depends(get_db)
) -> dict:
    service.create_user(db, create_user_request)
    return {"message": "User successfully created"}


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: UserLoginRequest,
    db: Session = Depends(get_db),
) -> dict:
    user = service.authenticate_user(form_data.username, form_data.password, db)
    token = service.create_access_token(user.username, user.id, timedelta(minutes=60))

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> dict:
    user = service.authenticate_user(form_data.username, form_data.password, db)
    token = service.create_access_token(user.username, user.id, timedelta(minutes=60))

    return {
        "access_token": token,
        "token_type": "bearer",
    }
