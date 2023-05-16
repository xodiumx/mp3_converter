from fastapi import FastAPI

from task_one.urls import router as quiz_router
from task_two.urls import router as users_router

tags_metadata = [
    {
        'name': 'quiz',
        'description': 'Quiz endpoints'
    },
    {
        'name': 'auth',
        'description': 'authentication and registration'
    },
    {
        'name': 'music',
        'description': 'music endpoints'
    },
]

app = FastAPI(
    title='Tasks',
    description='Test tasks for bewise.ai',
    version='0.0.1',
    openapi_tags=tags_metadata,
)

app.include_router(quiz_router)
app.include_router(users_router)
