from uuid import UUID

from fastapi import HTTPException

from app.Task2.database import Session
from app.Task2.utils import get_api_token


def valid_token(user_id: UUID, api_token: str) -> UUID:
    with Session() as session:
        if UUID(api_token) == get_api_token(user_id, session):
            return user_id
    raise HTTPException(status_code=401, detail="Invalid token")


def get_session() -> Session:
    with Session() as session:
        yield session
