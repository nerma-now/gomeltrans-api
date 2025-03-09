from fastapi import APIRouter
from config import settings
from .get_route_stops import router as get_route_stops_router


router: APIRouter = APIRouter(
    prefix=settings.app.api.v1.prefix,
)
router.include_router(get_route_stops_router)