import ast
import json
import logging
import random
from typing import Annotated

import starlette.status as status
import yaml
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
import time

from config import config
from database.models import (
    Tech_Question,
    Behavior_Question,
    Sessions,
    Interaction,
    CV,
    Personal_Question,
)
from database.setup import db_dependency
from inference.chat import Chat
from .auth import get_current_user
from .user import add_session_count

router = APIRouter(tags=["questions"])

user_dependency = Annotated[dict, Depends(get_current_user)]


logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


@router.get("/test")
def test():
    return {"message": "test"}


# GET Common Questions
@router.get("/common_question")
def get_common_questions(db: db_dependency, user: user_dependency) -> dict:
    # Check user session limit
    # if not user_session_available(db, user):
    # raise (HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User session limit reached"))

    tech_ids, tech_questions = get_tech_question_from_db(
        db, user, Tech_Question, config.TECH_QUESTION_NUM
    )
    behav_ids, behav_questions = get_question_from_db(
        db, Behavior_Question, config.BEHAV_QUESTION_NUM
    )

    store_questions(db, user, tech_ids, behav_ids)

    formatted_tech_questions = [
        {"id": q.id, "question": q.question} for q in tech_questions
    ]
    formatted_behav_questions = [
        {"id": q.id, "question": q.question} for q in behav_questions
    ]

    return {
        "tech_questions": formatted_tech_questions,
        "behav_questions": formatted_behav_questions,
    }


# GET Personal Question
@router.get("/personal_question")
async def get_personal_question(db: db_dependency, user: user_dependency):
    # Check user session limit
    # if not user_session_available(db, user):
    # raise (HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User session limit reached"))

    # add user session count + 1
    start = time.time()
    add_session_count(db, user)
    perQs = await generate_personal_question(db, user)
    # print("perQs:", perQs)
    personal_questions = get_asked_personal_questions(db, user)

    formatted_personal_questions = [
        {"id": q.id, "question": q.question, "criteria": q.criteria}
        for q in personal_questions
    ]
    end = time.time()
    print(f"{end - start} seconds")
    return {"personal_questions": formatted_personal_questions}


async def generate_personal_question(db, user):
    cv_content = db.query(CV.content).filter(CV.user_id == user.get("id")).first()[0]
    cv_position = db.query(CV.position).filter(CV.user_id == user.get("id")).first()[0]
    foundation_model = config.FOUNDATION_MODEL

    chat_model = Chat(
        foundation_model=foundation_model, content=cv_content, position=cv_position
    )

    perQ_results, _ = await chat_model.question_generation()
    print("perQ_results:", perQ_results)
    logging.info("Generating Question with api")
    logging.info(perQ_results)
    if perQ_results:
        perQ_json = ast.literal_eval(perQ_results)
        for item in perQ_json:
            question = item["question"]
            criteria = ",".join(item["criteria"])
            store_personal_questions(db, user, question, criteria)
        return perQ_json
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Personal question generation failed",
        )


def get_tech_question_from_db(
    db,
    user,
    Tech_Question,
    question_num,
):
    user_position = (
        db.query(CV.position).filter(CV.user_id == user.get("id")).first()[0]
    )
    
    all_question_ids = (
        db.query(Tech_Question.id).filter(Tech_Question.position == user_position).all()
    )
    try:
        ids = random.sample([qid[0] for qid in all_question_ids], k=question_num)
    except ValueError:
        print(user_position)
        print(all_question_ids)
        print("Not enough questions in database")
        raise ValueError
    query = db.query(Tech_Question).filter(Tech_Question.id.in_(ids)).all()

    return ids, query


def get_question_from_db(db, model, question_num):
    all_question_ids = db.query(model.id).all()
    ids = random.sample([qid[0] for qid in all_question_ids], k=question_num)
    query = db.query(model).filter(model.id.in_(ids)).all()

    return ids, query


def store_questions(db, user, tech_ids, behav_ids) -> str:
    new_interaction = Interaction(
        tech_questions=json.dumps(tech_ids),
        behav_questions=json.dumps(behav_ids),
        user_answers=json.dumps([]),
    )
    db.add(new_interaction)
    db.flush()

    new_session = Sessions(
        user_id=user.get("id"),
        cv_id=db.query(CV.id).filter(CV.user_id == user.get("id")).first()[0],
        interaction_id=new_interaction.id,
        feedback="",
    )
    db.add(new_session)
    db.commit()
    return {"message": "new interaction and session stored"}


def store_personal_questions(db, user, question, criteria) -> dict:
    curr_session_id = (
        db.query(Sessions.id)
        .filter(Sessions.user_id == user.get("id"))
        .order_by(Sessions.id.desc())
        .first()[0]
    )
    cv_id = db.query(CV.id).filter(CV.user_id == user.get("id")).first()[0]
    personal_question = Personal_Question(
        cv_id=cv_id,
        session_id=curr_session_id,
        question=question,
        criteria=criteria,
    )

    db.add(personal_question)
    db.flush()

    store_personal_Qid_in_interaction(db, user, personal_question.id)
    db.commit()
    return {"message": "personal question stored"}


def store_personal_Qid_in_interaction(db, user, personalQid):
    interaction_id = (
        db.query(Sessions.interaction_id)
        .filter(Sessions.user_id == user.get("id"))
        .order_by(Sessions.id.desc())
        .first()[0]
    )

    interaction_record = (
        db.query(Interaction).filter(Interaction.id == interaction_id).first()
    )

    personal_questions = (
        json.loads(interaction_record.personal_questions)
        if interaction_record.personal_questions
        else []
    )
    personal_questions.append(personalQid)
    interaction_record.user_answers = json.dumps(personal_questions)

    db.commit()


def get_asked_personal_questions(db, user):
    session_id = get_session_id(db, user)
    personal_questions = (
        db.query(Personal_Question)
        .filter(Personal_Question.session_id == session_id)
        .all()
    )
    return personal_questions


def get_session_id(db, user) -> int:
    session_id = (
        db.query(Sessions.id)
        .filter(Sessions.user_id == user.get("id"))
        .order_by(Sessions.id.desc())
        .first()[0]
    )
    return session_id
