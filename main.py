from fastapi import FastAPI
from config import settings
from src import router as main_router
from fastapi.staticfiles import StaticFiles
from src.exceptions.route_not_found import route_not_found_exception_handler
from src.controllers.gomeltrans_client.exceptions import RouteNotFoundException


def get_application() -> FastAPI:
    app: FastAPI = FastAPI(
        debug=settings.app.debug,
        title=settings.app.title,
        docs_url=settings.app.swagger.docs.prefix if settings.app.debug else None,
        redoc_url=settings.app.swagger.redoc.prefix if settings.app.debug else None,
    )

    app.add_exception_handler(RouteNotFoundException, route_not_found_exception_handler)

    app.mount('/src/static', StaticFiles(directory='src/static'), name='static')
    app.include_router(main_router)
    return app

app: FastAPI = get_application()