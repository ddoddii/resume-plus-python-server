from src.users.schemas import Users, CV
from src.models import Sessions
from src.inference.chat import Chat
import src.configs.config as config
from fastapi import HTTPException, status
from datetime import datetime


def upload_cv(cv_request, db, user):
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


def get_user_cv(db, user):
    cv_model = db.query(CV).filter(CV.user_id == user.get("id")).all()
    if cv_model is not None:
        return cv_model
    raise HTTPException(status_code=404, detail="CV not found")


def update_cv(cv_request, db, user, cv_id):
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


def delete_cv(db, user, cv_id):
    cv_model = (
        db.query(CV).filter(CV.id == cv_id).filter(CV.user_id == user.get("id")).first()
    )
    if cv_model is None:
        raise HTTPException(status_code=404, detail="CV not found")
    db.query(CV).filter(CV.id == cv_id).delete()
    db.commit()


def user_session_available(db, user):
    session_count = (
        db.query(Users).filter(Users.id == user.get("id")).first().session_count
    )
    return session_count < config.MAX_SESSION


def add_session_count(db, user):
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    user_model.session_count += 1
    db.commit()


def get_session_id(db, user) -> int:
    session_id = (
        db.query(Sessions.id)
        .filter(Sessions.user_id == user.get("id"))
        .order_by(Sessions.id.desc())
        .first()[0]
    )
    return session_id


def build_chat_model(db, user):
    cv_content = db.query(CV.content).filter(CV.user_id == user.get("id")).first()[0]
    cv_position = db.query(CV.position).filter(CV.user_id == user.get("id")).first()[0]
    chat_model = Chat(
        foundation_model=config.FOUNDATION_MODEL,
        content=cv_content,
        position=cv_position,
    )
    return chat_model
