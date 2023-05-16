from datetime import datetime

from pydantic import BaseModel


class Quiz(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime
