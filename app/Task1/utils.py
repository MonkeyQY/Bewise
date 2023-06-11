import logging
from typing import Optional, List

from aiohttp import ClientSession
from pydantic import ValidationError
from sqlalchemy import desc

from app.Task1 import config
from app.Task1.database import Session
from app.Task1.models import QuestionDB
from app.Task1.schemas import QuestionSchema

log = logging.getLogger("utils Task1")

format_string = "%Y-%m-%d %H:%M:%S"


class Questions:
    def __init__(self):
        self.questions = []
        self.count_exist_questions = 0

    @classmethod
    async def begin_receiving_questions(cls, count: int) -> None:
        self = cls()
        with Session() as session:
            await self._get_questions(count, session)

            await self._save_questions(session)

        log.info("Questions save")
        return None

    async def _get_questions(self, count: int, session: Session) -> None:
        self.count_exist_questions = 0
        async with ClientSession() as client:
            async with client.get(config.get_question_url(count)) as response:
                await self._check_exist_received_questions(await response.json())

        if self.count_exist_questions > 0:
            await self._get_questions(self.count_exist_questions, session)

        return None

    async def _check_exist_received_questions(self, questions: list) -> None:
        for question in questions:
            try:
                question = QuestionSchema.parse_obj(question)
            except ValidationError:
                log.info("Question not valid , question: %s", question)
                continue

            if not await self._is_question_exist(question):
                question.created_at = None
                if question not in self.questions:
                    self.questions.append(QuestionDB(**question.dict()))
                    continue

            self.count_exist_questions += 1

    async def _save_questions(self, session: Session) -> None:
        session.add_all(self.questions)
        session.commit()

    @staticmethod
    async def _is_question_exist(question: QuestionSchema, session: Session) -> bool:
        question = session.query(QuestionDB.id).get(question.id)
        return question is not None

    @staticmethod
    async def get_last_question() -> Optional[QuestionSchema]:
        with Session() as session:
            question = (
                session.query(QuestionDB)
                .order_by(desc(QuestionDB.created_at))
                .limit(1)
                .first()
            )

            if question is None:
                return None

            return QuestionSchema.parse_obj(question.__dict__)

    @staticmethod
    async def get_questions(count: int) -> Optional[List[QuestionSchema]]:
        with Session() as session:
            questions = (
                session.query(QuestionDB)
                .order_by(desc(QuestionDB.created_at))
                .limit(count)
                .all()
            )

            if questions is None:
                return None

            return [QuestionSchema.parse_obj(question.__dict__) for question in questions]
