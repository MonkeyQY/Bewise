import logging
from io import BytesIO
from typing import Iterator
from uuid import UUID

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from starlette.responses import StreamingResponse

from app.Task2 import config
from app.Task2.depends import valid_token
from app.Task2.schemas import AudioResponse, ResponseUser, CreateUser, RequestAddAudio
from app.Task2.utils import (
    convert_file_from_wav_to_mp3,
    save_audio,
    add_user,
    get_audio,
)

router = APIRouter()

log = logging.getLogger("router Task2")


@router.post(config.add_user_path, response_model=ResponseUser)
async def create_user(new_user: CreateUser) -> ResponseUser:
    log.info("Create user")

    user_id, api_token = await add_user(new_user.name)

    return ResponseUser(id=user_id, api_token=api_token)


async def check_valid_type_audio(file: UploadFile) -> None:
    if file.content_type != "audio/wav":
        raise HTTPException(status_code=400, detail="Invalid audio type")
    return None


@router.post(config.add_audio_path, response_model=AudioResponse)
async def add_audio(
        # user_id: str = Form(...),
        # api_token: str = Form(...),
        audio: UploadFile = File(...),
        user_id: UUID = Depends(valid_token)
) -> AudioResponse:
    log.info("Add audio : %s", user_id)

    await check_valid_type_audio(audio)
    mp3_audio = await convert_file_from_wav_to_mp3(audio)

    audio_id = await save_audio(user_id, mp3_audio)

    return AudioResponse(url=config.get_audio_url(user_id, audio_id))


@router.get(config.record_path, response_class=StreamingResponse)
async def record_audio(user_id: str, audio_id: str) -> StreamingResponse:
    audio_file: BytesIO = await get_audio(audio_id)

    if audio_file is None:
        raise HTTPException(status_code=404, detail="Audio not found")

    def generate() -> Iterator[bytes]:
        audio_file.seek(0)
        while chunk := audio_file.read(4096):
            yield chunk

    return StreamingResponse(generate(), media_type="audio/mp3")