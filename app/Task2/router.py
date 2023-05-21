import logging
from io import BytesIO
from typing import Iterator, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from starlette.responses import StreamingResponse

from app.Task2 import config
from app.Task2.depends import valid_token
from app.Task2.schemas import AudioResponse, ResponseUser, CreateUser
from app.Task2.utils import (
    convert_file_from_wav_to_mp3,
    save_audio,
    add_user,
    get_audio,
    check_valid_type_audio,
)

router = APIRouter()

log = logging.getLogger("router Task2")


@router.post(config.add_user_path, response_model=ResponseUser)
async def create_user(new_user: CreateUser) -> ResponseUser:
    log.info("Create user")

    user_id, api_token = await add_user(new_user.name)

    return ResponseUser(id=user_id, api_token=api_token)


@router.post(config.add_audio_path, response_model=AudioResponse)
async def add_audio(
    audio: UploadFile = File(...),
    user_id: UUID = Depends(valid_token),
) -> AudioResponse:
    log.info("Add audio : %s", user_id)

    await check_valid_type_audio(audio)
    mp3_audio = await convert_file_from_wav_to_mp3(audio)
    log.info("Audio convert to mp3")

    audio_id = await save_audio(user_id, mp3_audio)
    log.info("Audio save, id: %s", audio_id)
    return AudioResponse(url=config.get_audio_url(user_id, audio_id))


@router.get(config.record_path, response_class=StreamingResponse)
async def record_audio(user_id: str, audio_id: str) -> StreamingResponse:
    log.info("Get audio: %s for user : %s", audio_id, user_id)
    audio_file: Optional[BytesIO] = await get_audio(audio_id)

    if audio_file is None:
        log.info("Audio not found")
        raise HTTPException(status_code=404, detail="Audio not found")

    def generate() -> Iterator[bytes]:
        audio_file.seek(0)
        while chunk := audio_file.read(4096):
            yield chunk

    return StreamingResponse(generate(), media_type="audio/mp3")
