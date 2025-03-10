from fastapi import APIRouter
from src.controllers.gomeltrans_client.enums import TypeTransport
from src.controllers.gomeltrans_client.client import gomeltrans_client
from src.schemas.route import Routes


router: APIRouter = APIRouter()

@router.get(
    path='/get_routes',
    response_model=Routes
)
async def get_route_handler(
        type_transport: TypeTransport
) -> Routes:
    routes: Routes = await gomeltrans_client.get_routes(
        type_transport=type_transport
    )

    return routes
