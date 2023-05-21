import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_Task1 = {
    "drivername": "postgresql+psycopg2",
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
    "username": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASS", "postgres"),
    "database": os.environ.get("POSTGRES_DB_Task1", "Task1"),
}

get_question_num_path = os.environ.get("GET_QUESTION_NUM_PATH", "/get_question_num")

random_question_url = os.environ.get(
    "RANDOM_QUESTION_URL", "https://jservice.io/api/random?count="
)

prefix_task1 = os.environ.get("PREFIX_TASK1", "/task1")


def get_question_url(count: int) -> str:
    return random_question_url + str(count)
