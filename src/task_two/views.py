from uuid import UUID

from fastapi import Depends, APIRouter, UploadFile
from fastapi.responses import FileResponse

from sqlalchemy.ext.asyncio import AsyncSession

from main.db import get_async_session

from .models import User
from .utils import fastapi_users, MusicService


current_user = fastapi_users.current_user()

router = APIRouter(
    prefix='',
    tags=['music']
)


@router.post('/add-audio')
async def add_audio(
    user_id: UUID,
    audio_file: UploadFile,
    service: MusicService = Depends(),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
    ):
    """
    Функция создания аудиофайла:
        - Конвертирует файл из wav в mp3
        - Создаем запись в бд
        - Забираем последний созданный файл и его id
    """
    file = service.wav_to_mp3(audio_file)
    service.create_audio(file, user_id)
    await session.commit()
    audio = await service.get_all_user_audio(user.id)
    return {'detail': 'Аудиозапись успешно добавлена',
            'file_id': audio[-1].id
            }


@router.get('/download')
async def download_file(
    file_id: UUID,
    service: MusicService = Depends(),
    user: User = Depends(current_user),
    ):
    """
    Функция загрузки аудиофайла:
        - Получаем путь до файла
        - Передаем его в загрузку
    """
    audio_path = await service.get_audio_path(user.id, file_id)
    return FileResponse(
        audio_path, media_type='audio/mpeg', filename='audio.mp3')
