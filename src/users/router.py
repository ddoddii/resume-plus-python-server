from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session

from src.auth.service import get_current_user
from src.database import get_db
from src.users.schemas import CVRequest
import starlette.status as status
import src.users.service as userService


router = APIRouter(tags=["users"])


@router.post("/cv", status_code=status.HTTP_200_OK)
def upload_cv(
    cv_request: CVRequest, user=Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    return userService.upload_cv(cv_request, db, user)


@router.get("/cv", status_code=status.HTTP_200_OK)
def get_user_cv(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return userService.get_user_cv(db, user)


@router.put("/cv/{cv_id}", status_code=status.HTTP_200_OK)
def update_cv(
    cv_request: CVRequest,
    cv_id: int = Path(gt=0),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    userService.update_cv(cv_request, db, user, cv_id)
    return {"message": "CV update success"}


@router.delete("/cv/{cv_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cv(
    cv_id: int = Path(gt=0),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    userService.delete_cv(db, user, cv_id)
    return {"message": "CV delete success"}
