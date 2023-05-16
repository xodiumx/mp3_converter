from fastapi import FastAPI
from sqladmin import Admin

from task_one.urls import router as task_one


tags_metadata = [
    {
        'name': 'quiz',
        'description': 'Quiz endpoints'
    },
]

app = FastAPI(
    title='Tasks',
    description='Test tasks for bewise.ai',
    version='0.0.1',
    openapi_tags=tags_metadata,
)

app.include_router(task_one)
