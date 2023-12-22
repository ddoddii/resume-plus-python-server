from datetime import datetime
from enum import Enum
from typing import Annotated

import starlette.status as status
import yaml
from fastapi import APIRouter, HTTPException, Path, Depends
from pydantic import BaseModel, Field

from config import config
from database.models import Users, CV
from database.setup import db_dependency
from inference.chat import Chat
from .auth import get_current_user

router = APIRouter(tags=["user"])


user_dependency = Annotated[dict, Depends(get_current_user)]


class Position(str, Enum):
    ai = "ai"
    be = "be"
    fe = "fe"
    mobile = "mobile"


class UserRequest(BaseModel):
    username: str
    name: str
    email: str
    password: str = Field(min_length=4)


class CVRequest(BaseModel):
    content: str
    position: Position


@router.post("/cv", status_code=status.HTTP_200_OK)
async def upload_cv(cv_request: CVRequest, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )

    formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv_model = CV(
        **cv_request.dict(), upload_time=formatted_datetime, user_id=user.get("id")
    )

    db.add(cv_model)
    db.commit()
    return {"message": "CV upload success"}


@router.get("/cv", status_code=status.HTTP_200_OK)
async def get_user_cv(db: db_dependency, user: user_dependency):
    cv_model = db.query(CV).filter(CV.user_id == user.get("id")).all()
    if cv_model is not None:
        return cv_model
    raise HTTPException(status_code=404, detail="CV not found")


@router.put("/cv/{cv_id}", status_code=status.HTTP_200_OK)
async def update_cv(
    cv_request: CVRequest,
    db: db_dependency,
    user: user_dependency,
    cv_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    cv_model = (
        db.query(CV).filter(CV.id == cv_id).filter(CV.user_id == user.get("id")).first()
    )
    if cv_model is None:
        raise HTTPException(status_code=404, detail="CV not found")
    cv_model.content = cv_request.content
    cv_model.position = cv_request.position
    db.commit()
    return {"message": "CV update success"}


@router.delete("/cv/{cv_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cv(db: db_dependency, user: user_dependency, cv_id: int = Path(gt=0)):
    cv_model = (
        db.query(CV).filter(CV.id == cv_id).filter(CV.user_id == user.get("id")).first()
    )
    if cv_model is None:
        raise HTTPException(status_code=404, detail="CV not found")
    db.query(CV).filter(CV.id == cv_id).delete()
    db.commit()
    return {"message": "CV delete success"}


def build_chat_model(db: db_dependency, user: user_dependency):
    cv_content = db.query(CV.content).filter(CV.user_id == user.get("id")).first()[0]
    cv_position = db.query(CV.position).filter(CV.user_id == user.get("id")).first()[0]
    chat_model = Chat(
        foundation_model=config.FOUNDATION_MODEL,
        content=cv_content,
        position=cv_position,
    )
    return chat_model


def user_session_available(db: db_dependency, user: user_dependency):
    session_count = (
        db.query(Users).filter(Users.id == user.get("id")).first().session_count
    )
    return session_count < config.MAX_SESSION


def add_session_count(db: db_dependency, user: user_dependency):
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    user_model.session_count += 1
    db.commit()
