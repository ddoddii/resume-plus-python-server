from fastapi import APIRouter, HTTPException, Depends
from src.questions import service
from sqlalchemy.orm import Session
from src.auth.service import get_current_user
from src.database import get_db


router = APIRouter(tags=["questions"])


@router.get("/common_question")
def get_common_question(
    user=Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return service.get_common_questions(db, user)


@router.get("/personal_question")
def get_personal_question(
    user=Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return service.get_personal_questions(db, user)
