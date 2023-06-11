import logging

from fastapi import APIRouter, BackgroundTasks

from app.Task1 import config
from app.Task1.schemas import QuestionNum, QuestionsSchema
from app.Task1.utils import Questions

router = APIRouter()

log = logging.getLogger("router Task1")


@router.post(config.get_question_num_path, response_model=QuestionsSchema)
async def get_count_questions(
    num: QuestionNum, background_tasks: BackgroundTasks
) -> QuestionsSchema:
    log.info("Get question num: %s", num)

    background_tasks.add_task(Questions.begin_receiving_questions, num.questions_num)

    last_questions = await Questions.get_last_questions(num.questions_num)
    log.info("Get questions: %s", last_questions)
    return QuestionsSchema(questions=last_questions)
