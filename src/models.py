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


class Sessions(Base):
    __tablename__ = "session"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    cv_id = Column(Integer, ForeignKey("cv.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    interaction_id = Column(Integer, ForeignKey("interaction.id"), nullable=False)
    feedback = Column(Text)


class Interaction(Base):
    __tablename__ = "interaction"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    tech_questions = Column(Text)
    behav_questions = Column(Text)
    personal_questions = Column(Text)
    user_answers = Column(Text)
