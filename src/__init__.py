from fastapi import APIRouter
from .api import router as api_router

router: APIRouter = APIRouter()
router.include_router(api_router)
