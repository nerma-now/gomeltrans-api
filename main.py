from fastapi import FastAPI
from config import settings
from src import router as main_router
from fastapi.staticfiles import StaticFiles


app: FastAPI = FastAPI(
    debug=settings.app.debug,
    title=settings.app.title,
    docs_url=settings.app.swagger.docs.prefix if settings.app.debug else None,
    redoc_url=settings.app.swagger.redoc.prefix if settings.app.debug else None,
)


app.mount('/src/static', StaticFiles(directory='src/static'), name='static')
app.include_router(main_router)