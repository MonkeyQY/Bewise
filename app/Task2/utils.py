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
    try:
        audio = AudioSegment.from_wav(audio.file)
        memory = BytesIO()
        audio.export(memory, format="mp3")
    except Exception as e:
        log.info("Error convert audio: %s", e)
        raise HTTPException(status_code=400, detail="Error convert audio")
    return memory


async def save_audio(user_id: UUID, audio: BytesIO, session: Session) -> Audio:
    audio_data = audio.read()
    try:
        audio = Audio(user_id=user_id, audio=audio_data)
        session.add(audio)
    except Exception as e:
        log.info("Error save audio: %s", e)
        raise HTTPException(status_code=400, detail="Error save audio")
    return audio


async def add_user(name: str, session: Session) -> User:
    user = User(name=name)
    session.add(user)
    return user


async def get_audio(audio_id: str, session: Session) -> Optional[BytesIO]:
    audio = session.query(Audio).get(audio_id)
    if not audio:
        return None

    return BytesIO(audio.audio)


def get_api_token(user_id: UUID, session: Session) -> Optional[UUID]:
    api_token = session.query(User.api_token).filter(User.id == user_id).first()
    log.info("Get api token: %s", api_token)
    return api_token[0]
