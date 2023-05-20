import os
from uuid import UUID

from dotenv import load_dotenv

from app import config

load_dotenv()

DATABASE_Task2 = {
    "drivername": "postgresql+psycopg2",
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
    "username": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASS", "postgres"),
    "database": os.environ.get("POSTGRES_DB", "Task2"),
}

audio_url = os.environ.get("AUDIO_URL", f"http://localhost:{config.port}")

prefix_task2 = os.environ.get("PREFIX_TASK2", "/task2")

record_path = os.environ.get("RECORD_PATH", "/record")


def get_audio_url(user_id: UUID, audio_id: UUID) -> str:
    return f"{audio_url}{prefix_task2}{record_path}?user_id={user_id}&audio_id={audio_id}"


add_audio_path = os.environ.get("ADD_AUDIO_PATH", "/add_audio")

add_user_path = os.environ.get("ADD_USER_PATH", "/add_user")
