from config import settings
from fastapi import FastAPI
from src import router as main_router
from starlette.staticfiles import StaticFiles
from src.swagger.swagger import register_static_docs_routes
from src.exceptions.route_not_found import route_not_found_exception_handler
from src.controllers.gomeltrans_client.exceptions import RouteNotFoundException


def get_application() -> FastAPI:
    application: FastAPI = FastAPI(
        debug=settings.app.debug,
        title=settings.app.title,
        docs_url=None,
        redoc_url=None
    )

    application.add_exception_handler(
        exc_class_or_status_code=RouteNotFoundException,
        handler=route_not_found_exception_handler
    )

    application.mount(
        path=settings.app.swagger.static_path,
        app=StaticFiles(directory=settings.app.swagger.mount_path),
        name='static'
    )
    application.include_router(
        router=main_router
    )

    if settings.app.debug:
        register_static_docs_routes(application)

    return application