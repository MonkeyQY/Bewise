from uuid import UUID

from pydantic import BaseModel


class UserDB(BaseModel):
    id: str
    name: str
    api_token: str


class AudioDB(BaseModel):
    id: str
    user_id: str
    audio: bytes


class RequestAddAudio(BaseModel):
    user_id: str
    api_token: str


class AudioResponse(BaseModel):
    url: str


class CreateUser(BaseModel):
    name: str


class ResponseUser(BaseModel):
    id: UUID
    api_token: UUID
