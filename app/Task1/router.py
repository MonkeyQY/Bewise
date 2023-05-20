import logging
from typing import Optional

from fastapi import APIRouter, BackgroundTasks

from app.Task1 import config
from app.Task1.schemas import QuestionNum, Question
from app.Task1.utils import get_questions, get_last_question

router = APIRouter()

log = logging.getLogger("router Task1")


@router.post(config.get_question_num_path, response_model=Optional[Question])
async def get_question_num(
    num: QuestionNum, background_tasks: BackgroundTasks
) -> Optional[Question]:
    log.info("Get question num: %s", num)
    background_tasks.add_task(get_questions, num.questions_num)
    return await get_last_question()
