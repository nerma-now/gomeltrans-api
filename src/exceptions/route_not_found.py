from fastapi import status
from starlette.responses import JSONResponse


async def route_not_found_exception_handler(request, exc):
    return JSONResponse(
        content={'message': str(exc)},
        status_code=status.HTTP_404_NOT_FOUND,
    )