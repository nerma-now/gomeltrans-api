from config import settings
from fastapi import FastAPI
from starlette.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html, get_redoc_html


def register_static_docs_routes(app: FastAPI):
    @app.get(
        path='/docs',
        include_in_schema=False
    )
    async def custom_swagger_ui_html_handler() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f'{settings.app.title} - {settings.app.swagger.docs.title}',
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=f'{settings.app.swagger.static_path}/swagger-ui-bundle.js',
            swagger_css_url=f'{settings.app.swagger.static_path}/swagger-ui.css',
        )

    @app.get(app.swagger_ui_oauth2_redirect_url,
             include_in_schema=False)
    async def swagger_ui_redirect() -> HTMLResponse:
        return get_swagger_ui_oauth2_redirect_html()

    @app.get(
        path='/redoc',
        include_in_schema=False
    )
    async def redoc_html() -> HTMLResponse:
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=f'{settings.app.title} - {settings.app.swagger.redoc.title}',
            redoc_js_url=f'{settings.app.swagger.static_path}/redoc.standalone.js',
        )