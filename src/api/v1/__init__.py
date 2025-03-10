from fastapi import APIRouter
from config import settings
from .get_route_stops import router as get_route_stops_router
from .get_routes import router as get_routes_router


router: APIRouter = APIRouter(
    prefix=settings.app.api.v1.prefix,
)
router.include_router(get_route_stops_router)
router.include_router(get_routes_router)