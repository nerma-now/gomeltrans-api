from fastapi import APIRouter
from config import settings
from .test import router as test_router


router: APIRouter = APIRouter(
    prefix=settings.app.api.v1.prefix,
)
router.include_router(test_router)