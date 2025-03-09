from http import HTTPStatus
from fastapi import APIRouter
from src.controllers.gomeltrans_client.client import gomeltrans_client
from src.schemas.responses import Message
from src.schemas.stop import RouteStops
from src.controllers.gomeltrans_client.enums import TypeTransport

router: APIRouter = APIRouter()

@router.get(
    path='/get_route_stops',
    response_model=RouteStops,
    responses={
        HTTPStatus.NOT_FOUND.value: {"model": Message},
    }
)
async def get_route_stops_handler(
        type_transport: TypeTransport,
        number: str,
) -> RouteStops:

    route_stops: RouteStops = await gomeltrans_client.get_route_stops(
        type_transport=type_transport,
        number=number
    )
    return route_stops

