import ast
import time
import json
import random
import logging
from sqlalchemy import desc
from fastapi import HTTPException, status

from src.questions.schemas import Tech_Question, Behavior_Question, Personal_Question
import src.configs.config as config
from src.models import Sessions, Interaction
from src.users.schemas import CV
from src.users.service import add_session_count
from src.inference.chat import Chat


def get_common_questions(db, user) -> dict:
    tech_ids, tech_questions = get_tech_question_from_db(
        db, user, config.TECH_QUESTION_NUM
    )
    behav_ids, behav_questions = get_behav_question_from_db(
        db, config.BEHAV_QUESTION_NUM
    )

    store_common_questions(db, user, tech_ids, behav_ids)

    formatted_tech_questions = [
        {"id": q.id, "questions": q.question} for q in tech_questions
    ]
    formatted_behav_questions = [
        {"id": q.id, "questions": q.question} for q in behav_questions
    ]

    return {
        "tech_questions": formatted_tech_questions,
        "behav_questions": formatted_behav_questions,
    }


def get_tech_question_from_db(
    db,
    user,
    question_num,
):
    user_position = (
        db.query(CV.position).filter(CV.user_id == user.get("id")).first()[0]
    )
    all_question_ids = (
        db.query(Tech_Question.id).filter(Tech_Question.position == user_position).all()
    )
    ids = random.sample([qid[0] for qid in all_question_ids], k=question_num)
    query = db.query(Tech_Question).filter(Tech_Question.id.in_(ids)).all()

    return ids, query


def get_behav_question_from_db(db, question_num):
    all_question_ids = db.query(Behavior_Question.id).all()
    ids = random.sample([qid[0] for qid in all_question_ids], k=question_num)
    query = db.query(Behavior_Question).filter(Behavior_Question.id.in_(ids)).all()

    return ids, query


def store_common_questions(db, user, tech_ids, behav_ids) -> str:
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


def get_personal_questions(db, user) -> dict:
    # add users session count + 1
    start = time.time()
    add_session_count(db, user)
    perQs = generate_personal_question(db, user)
    # print("perQs:", perQs)
    personal_questions = get_asked_personal_questions(db, user)

    formatted_personal_questions = [
        {"id": q.id, "questions": q.question, "criteria": q.criteria}
        for q in personal_questions
    ]
    end = time.time()
    print(f"{end - start} seconds")
    return {"personal_questions": formatted_personal_questions}


def generate_personal_question(db, user):
    cv_content = (
        db.query(CV.content)
        .filter(CV.user_id == user.get("id"))
        .order_by(desc(CV.upload_time))
        .first()[0]
    )
    cv_position = (
        db.query(CV.position)
        .filter(CV.user_id == user.get("id"))
        .order_by(desc(CV.upload_time))
        .first()[0]
    )
    foundation_model = config.FOUNDATION_MODEL

    chat_model = Chat(
        foundation_model=foundation_model, content=cv_content, position=cv_position
    )

    perQ_results, _ = chat_model.question_generation()

    logging.info("Generating Personal Question with api...")
    logging.info(perQ_results)

    if perQ_results:
        perQ_json = json.loads(perQ_results)
        print(type(perQ_json))
        for item in perQ_json:
            question = item["question"]
            criteria = ",".join(item["criteria"])
            store_personal_questions(db, user, question, criteria)
        return perQ_json
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Personal questions generation failed",
        )


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
    return {"message": "personal questions stored"}


def store_personal_Qid_in_interaction(db, user, personalQid):
    interaction_id = (
        db.query(Sessions.interaction_id)
        .filter(Sessions.user_id == user.get("id"))
        .order_by(Sessions.id.desc())
        .first()[0]
    )


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
