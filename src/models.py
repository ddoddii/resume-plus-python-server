from sqlalchemy import Column, Integer, String, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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
