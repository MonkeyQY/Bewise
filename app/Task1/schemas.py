from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class QuestionNum(BaseModel):
    questions_num: int


class Category(BaseModel):
    id: int
    title: str
    created_at: str
    updated_at: str
    clues_count: int


class QuestionSchema(BaseModel):
    id: int
    answer: str
    question: str
    value: Optional[int]
    airdate: str
    created_at: str | datetime
    updated_at: str
    category_id: int
    game_id: int
    invalid_count: Optional[int]
    category: Category


class QuestionsSchema(BaseModel):
    questions: Optional[list[QuestionSchema]]


class QuestionModelDB(BaseModel):
    id: int
    answer: str
    question: str
    value: int
    airdate: datetime
    created_at: datetime
    updated_at: datetime
    category_id: int
    game_id: int
    invalid_count: Optional[int]
    category: Category
