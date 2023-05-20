from typing import Optional, List

from aiohttp import ClientSession
from sqlalchemy import desc

from app.Task1 import config
from app.Task1.database import Session
from app.Task1.models import QuestionDB
from app.Task1.schemas import Question

format_string = "%Y-%m-%d %H:%M:%S"


async def save_questions(questions: List[QuestionDB]) -> None:
    with Session() as session:
        session.add_all(questions)
        session.commit()


async def get_questions(count: int) -> None:
    not_exist_questions = []
    count_exist_questions = 0
    async with ClientSession() as client:
        async with client.get(config.get_question_url(count)) as response:
            for question in await response.json():
                question = Question.parse_obj(question)

                if not await is_question_exist(question):
                    question.created_at = None
                    if question.id not in not_exist_questions:
                        not_exist_questions.append(QuestionDB(**question.dict()))

                count_exist_questions += 1
    await save_questions(not_exist_questions)
    if count_exist_questions > 0:
        await get_questions(count_exist_questions)
    return None


async def is_question_exist(question: Question) -> bool:
    with Session() as session:
        question = session.query(QuestionDB).get(question.id)
    return question is not None


async def get_last_question() -> Optional[Question]:
    with Session() as session:
        question = (
            session.query(QuestionDB)
            .order_by(desc(QuestionDB.created_at))
            .limit(1)
            .first()
        )
        question.created_at = str(question.created_at)
        return Question.parse_obj(question.__dict__)
