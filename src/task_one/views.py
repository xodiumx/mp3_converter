import requests

from fastapi import Depends, APIRouter, HTTPException, status, Query

from sqlalchemy.ext.asyncio import AsyncSession

from main.db import get_async_session
from .schemas import Quiz
from .utils import QuizService

router = APIRouter(
    prefix='',
    tags=['quiz']
)


@router.post('/quiz', response_model=Quiz)
async def create_quiz(
    questions_num: int = Query(..., gt=0, le=20),
    service: QuizService = Depends(),
    session: AsyncSession = Depends(get_async_session),
    ):
    """
    - Функция создания вопросов:
        - query parametrs:
          1. questions_num - количество запрашеваемых вопросов от 1 до 20
    - Вопросы создаются пока их количество не уменьшиться до 0.
    - Возвращает последний созданный вопрос.
    """
    while questions_num != 0:
        endpoint = f'https://jservice.io/api/random?count={questions_num}'

        try: 
            response = requests.get(endpoint)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Упс, непредвиденная ошибочка)')

        response, questions_num = service.create_questions(response.json(), 
                                                           questions_num)
        await session.commit()
    last_created_question = response[-1]
    return Quiz(**service.get_info_about_one(last_created_question))
