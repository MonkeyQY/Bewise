import logging
from io import BytesIO
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from fastapi import UploadFile
from pydub import AudioSegment

from app.Task2.database import Session
from app.Task2.models import Audio, User

log = logging.getLogger("utils Task2")


async def check_valid_type_audio(file: UploadFile) -> None:
    if file.content_type != "audio/wav":
        log.info("Invalid audio type")
        raise HTTPException(status_code=400, detail="Invalid audio type")
    return None


async def convert_file_from_wav_to_mp3(audio: UploadFile) -> BytesIO:
    audio = AudioSegment.from_wav(audio.file)
    memory = BytesIO()
    audio.export(memory, format="mp3")
    return memory


async def save_audio(user_id: UUID, audio: BytesIO) -> UUID:
    audio_data = audio.read()

    with Session() as session:
        audio = Audio(user_id=user_id, audio=audio_data)
        session.add(audio)
        session.commit()
        return audio.id


async def add_user(name: str) -> tuple[UUID, UUID]:
    with Session() as session:
        user = User(name=name)
        session.add(user)
        session.commit()
        return user.id, user.api_token


async def get_audio(audio_id: str) -> Optional[BytesIO]:
    with Session() as session:
        audio = session.query(Audio).get(audio_id)
        if not audio:
            return None

        return BytesIO(audio.audio)


def get_api_token(user_id: UUID) -> UUID:
    with Session() as session:
        user = session.query(User).get(user_id)
        return user.api_token
