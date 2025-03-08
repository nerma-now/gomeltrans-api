from fastapi import APIRouter
from config import settings
from .v1 import router as v1_router


router: APIRouter = APIRouter(
    prefix=settings.app.api.prefix,
)
router.include_router(v1_router)