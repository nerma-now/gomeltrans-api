from fastapi import APIRouter
from .api import router as api_router
# from .swagger import router as swagger_router


router: APIRouter = APIRouter()
router.include_router(api_router)
