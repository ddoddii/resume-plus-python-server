from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
import starlette.status as status
from datetime import timedelta, datetime
from jose import jwt, JWTError
from typing import Annotated

from src.users.schemas import Users
import src.configs.config as config


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_user(db, create_user_request):
    check_duplicate_username(db, create_user_request.username)
    create_user_model = Users(
        username=create_user_request.username,
        name=create_user_request.name,
        email=create_user_request.email,
        hashed_password=bcrypt_context.hash(create_user_request.password),
    )

    db.add(create_user_model)
    db.commit()


def check_duplicate_username(db, request_username):
    existing_user = db.query(Users).filter(Users.username == request_username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not find username"
        )
    if not bcrypt_context.verify(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
    return user


def create_access_token(username: str, user_id: int, expires_data: timedelta):
    encode = {"sub": username, "id": user_id}
    expire = datetime.utcnow() + expires_data
    encode.update({"exp": expire})
    return jwt.encode(encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


def get_current_user(token: str = Depends(oauth2_bearer)) -> dict:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate users",
            )
        return {
            "username": username,
            "id": user_id,
        }
    except JWTError:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate users"
        )
