import logging
from typing import Optional

from aiohttp import ClientSession
from sqlalchemy import desc

from app.Task1 import config
from app.Task1.database import Session
from app.Task1.models import QuestionDB
from app.Task1.schemas import Question

log = logging.getLogger("utils Task1")

format_string = "%Y-%m-%d %H:%M:%S"


class Questions:
    def __init__(self):
        self.questions = []
        self.count_exist_questions = 0

    @classmethod
    async def begin_receiving_questions(cls, count: int) -> None:
        self = cls()
        await self._get_questions(count)

        await self._save_questions()
        log.info("Questions save")
        return None

    async def _get_questions(self, count: int) -> None:
        self.count_exist_questions = 0
        async with ClientSession() as client:
            async with client.get(config.get_question_url(count)) as response:
                await self.check_exist_received_questions(await response.json())

        if self.count_exist_questions > 0:
            await self._get_questions(self.count_exist_questions)

        return None

    async def check_exist_received_questions(self, questions: list) -> None:
        for question in questions:
            try:
                question = Question.parse_obj(question)
            except ValueError:
                log.info("Question not valid , question: %s", question)
                continue

            if not await self._is_question_exist(question):
                question.created_at = None
                if question not in self.questions:
                    self.questions.append(QuestionDB(**question.dict()))
                    continue

            self.count_exist_questions += 1

    async def _save_questions(self) -> None:
        with Session() as session:
            session.add_all(self.questions)
            session.commit()

    @staticmethod
    async def _is_question_exist(question: Question) -> bool:
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
