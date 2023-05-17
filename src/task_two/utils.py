import os
import uuid
import ffmpeg

from fastapi import Depends, HTTPException, UploadFile, status
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)
from pydub import AudioSegment
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from main.db import get_async_session
from main.settings import settings

from .manage import get_user_manager
from .models import AudioFile, User

SECRET = settings.secret_key


def get_jwt_strategy() -> JWTStrategy:
    """Получение JWT - токена."""
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


cookie_transport = CookieTransport(
    cookie_name='auth', cookie_max_age=3600)

auth_backend = AuthenticationBackend(
    name='jwt',
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


class MusicService:

    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session)
    ) -> None:
        self.session = session

    def wav_to_mp3(self, file: UploadFile) -> dict:
        """
        Конвертация аудиофайла из wav в mp3:
            - Создаем файл wav
            - Конвертируем его в mp3
            - Удаляем файл wav
        """
        file_name, ext = file.filename.split('.')

        if ext != 'wav':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Расширение аудиофайла должно быть '
                                       'формата "wav"')

        wav_path = os.path.join(f'media/{file_name}.wav')
        mp3_path = os.path.join(f'media/{file_name}.mp3')
        ffmpeg_path = os.path.join(
            'static/ffmpeg-6.0-full_build/bin/ffmpeg.exe')

        with open(wav_path, 'wb') as temp_wav:
            temp_wav.write(file.file.read())

        #AudioSegment.converter = ffmpeg_path # for windows 
        audio = AudioSegment.from_wav(wav_path)
        audio.export(mp3_path, format='mp3')

        os.remove(wav_path)

        return {'mp3_path': mp3_path, 'file_name': file_name}

    def create_audio(
        self,
        audio_file: dict,
        user_id: uuid.UUID,
    ) -> dict:
        with open(audio_file.get('mp3_path'), 'rb') as file:
            audio = AudioFile(
                user=user_id,
                file_path=audio_file.get('mp3_path'),
                filename=audio_file.get('file_name'),
                data=file.read(),
            )
            self.session.add(audio)
        return audio

    async def get_all_user_audio(
        self,
        user_id: uuid.UUID,
    ) -> list[AudioFile]:
        """Функция получения всех записей пользователя."""
        audio = (
            await
            self.session
            .execute(
                select(AudioFile)
                .filter_by(
                    user=user_id,
                )
            )
        )
        return audio.scalars().all()

    async def get_audio_path(
        self,
        user_id: uuid.UUID,
        file_id: uuid.UUID,
    ):
        """Функция получения пути до аудиофайла."""
        audio_path = (
            await
            self.session
            .execute(
                select(AudioFile)
                .filter_by(
                    id=file_id,
                    user=user_id,
                )
            )
        )
        return audio_path.scalars().one().file_path
