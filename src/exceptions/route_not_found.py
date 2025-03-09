from http import HTTPStatus
from starlette.responses import JSONResponse


async def route_not_found_exception_handler(request, exc):
    print(type(exc), type(request))
    return JSONResponse(
        content={'message': str(exc)},
        status_code=HTTPStatus.NOT_FOUND,
    )