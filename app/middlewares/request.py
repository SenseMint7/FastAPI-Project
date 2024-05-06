from typing import Awaitable, Callable, Union

from fastapi import Request
from starlette.responses import JSONResponse, StreamingResponse

from app.config import settings
from app.errors.exceptions import APIException


async def base_http_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[StreamingResponse]]
) -> Union[StreamingResponse, JSONResponse]:
    url = request.url.path

    if url in settings.EXCEPT_PATH_LIST:
        response: StreamingResponse = await call_next(request)
        return response

    try:
        response = await call_next(request)
        return response
    except Exception as e:
        error = await exception_handler(e)
        error_dict = {
            "status_code": error.status_code,
            "code": error.code,
            "message": error.message,
        }
        return JSONResponse(status_code=error.status_code, content=error_dict)


async def exception_handler(error: Exception) -> APIException:
    if not isinstance(error, APIException):
        error = APIException()
    return error
