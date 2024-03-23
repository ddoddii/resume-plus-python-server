from sqlalchemy import Column, Integer, String, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Tech_Question(Base):
    __tablename__ = "tech_question"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    question = Column(Text, nullable=False)
    position = Column(String(20))
    topic = Column(String(20))
    example_answer = Column(Text)


class Behavior_Question(Base):
    __tablename__ = "behavior_question"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    question = Column(Text, nullable=False)
    criteria = Column(String(20))


class Personal_Question(Base):
    __tablename__ = "personal_question"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    cv_id = Column(Integer, ForeignKey("cv.id"))
    session_id = Column(Integer, ForeignKey("session.id"))
    question = Column(Text, nullable=False)
    criteria = Column(Text)
