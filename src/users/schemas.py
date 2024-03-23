from enum import Enum
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True, index=True)
    username = Column(String(20), nullable=False, index=True, unique=True)
    name = Column(String(20), nullable=False)
    hashed_password = Column(String(64), nullable=False)
    email = Column(String(30))
    session_count = Column(Integer, default=0)


class CV(Base):
    __tablename__ = "cv"

    id = Column(Integer, nullable=False, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    position = Column(String(20), nullable=True)
    upload_time = Column(Text, nullable=False)


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
