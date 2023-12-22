from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import Annotated

# TODO: 디비 위치 숨기기
# 이건 .env 파일로 옮기면 이 디비를 바라보는 모든 코드를 수정할 필요 없는 장점도 있음.
SQLALCEMY_DATABASE_URL = 'sqlite:///./resume_ai_chat.db'

engine = create_engine(SQLALCEMY_DATABASE_URL,connect_args={'check_same_thread':False})

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

db_dependency = Annotated[Session, Depends(get_db)]
