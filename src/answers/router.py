from fastapi import APIRouter, Depends
import starlette.status as status
from sqlalchemy.orm import Session

from src.answers import service
from src.answers.schemas import SingleAnswer, SingleResponse, AskedQuestionsResponse
from src.auth.service import get_current_user
from src.database import get_db

router = APIRouter(tags=["answers"])


@router.get("/asked_question")
def get_asked_question(
    user=Depends(get_current_user), db: Session = Depends(get_db)
) -> AskedQuestionsResponse:
    return service.get_asked_question(db, user)


@router.post("/submit_tech_answer/{question_id}", status_code=status.HTTP_200_OK)
def submit_tech_answer(
    question_id: int,
    request: SingleAnswer,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SingleResponse:
    return service.submit_tech_answer(question_id, request, db, user)


@router.post("/submit_behav_answer/{question_id}", status_code=status.HTTP_200_OK)
def submit_behav_answer(
    question_id: int,
    request: SingleAnswer,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SingleResponse:
    return service.submit_behav_answer(question_id, request, db, user)


@router.post("/submit_personal_answer/{question_id}", status_code=status.HTTP_200_OK)
def submit_personal_answer(
    question_id: int,
    request: SingleAnswer,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SingleResponse:
    return service.submit_personal_answer(question_id, request, db, user)
