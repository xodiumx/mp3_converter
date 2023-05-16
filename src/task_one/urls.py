from fastapi import APIRouter

from .views import router as views


router = APIRouter()

router.include_router(views)
