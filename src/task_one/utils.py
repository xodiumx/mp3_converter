from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from main.db import get_async_session

from .models import QuizModel


class QuizService:

    def __init__(self, session: Session = Depends(get_async_session)) -> None:
        self.session = session

    def get_info_about_many(
        self,
        response: list[dict],
        ) -> list[dict]:
        """
        Получение информации о нескольких вопросах:
          - принимает объекты вопросов
          - возвращает сформированные вопросы с полями:
            1. текст вопроса
            2. текст ответа
            3. id вопроса
            4. дата создания вопроса
            и количество уникальных вопросов.
        """
        questions = [
            {
                'id': question.get('id'),
                'question': question.get('question'),
                'answer': question.get('answer'),
                'created_at': datetime.strptime(
                        question.get('created_at'),
                        '%Y-%m-%dT%H:%M:%S.%f%z')
            }
            for question in response
        ]
        uniques_ids = {question.get('id') for question in questions}
        return questions, len(uniques_ids)
    
    def get_info_about_one(self, question: QuizModel) -> dict:
        """Получение информации об одном вопросе."""
        return {
                'id': question.id,
                'question': question.question,
                'answer': question.answer,
                'created_at': question.created_at
            }

    def create_questions(
        self, 
        response: list[dict], 
        questions_num: int
        ) -> dict:
        """
        Функция создания вопросов в базе:
        - принимает объекты вопросов и их количество
        - возвращает созданные вопросы и количество не созданных вопросов
        """
        questions, created_questions = self.get_info_about_many(response)
        questions = [
            QuizModel(**question)
            for question in questions
        ]
        self.session.add_all(questions)
        return questions, questions_num - created_questions
