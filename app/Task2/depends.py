from uuid import UUID

from fastapi import HTTPException

from app.Task2.utils import get_api_token


def valid_token(user_id: UUID, api_token: UUID) -> UUID:
    if api_token == get_api_token(user_id):
        return user_id
    raise HTTPException(status_code=401, detail="Invalid token")
