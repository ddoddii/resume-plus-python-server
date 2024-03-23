from enum import Enum
from pydantic import BaseModel, Field
from typing import Annotated, Dict, List


class QuestionType(str, Enum):
    tech = "techQ"
    behav = "behavQ"
    personal = "perQ"


class SingleAnswer(BaseModel):
    answer: str = Field(default="I DON'T KNOW")


class SingleResponse(BaseModel):
    type: QuestionType
    question: str
    user_answer: str
    evaluation: Dict


class AskedQuestionsResponse(BaseModel):
    techQ_ids: List[int]
    behavQ_ids: List[int]
    perQ_ids: List[int]
