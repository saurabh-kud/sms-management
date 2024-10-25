from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.services.response import APIResponse
from app.error.custom_exception import CustomException


def _prepare_response(status: int, exc: Any) -> JSONResponse:
    response = APIResponse()
    response.status = status

    if isinstance(exc, RequestValidationError):
        error = exc.errors()[0]
        message = error["msg"]
        error_type = error["type"]

        if error_type == "missing":
            field = error["loc"][1:]
            msg = f"'{'.'.join(map(str, field))}' is not provided."
        elif error_type == "value_error":
            msg = message.split(",")[1].strip()
        else:
            field = error["loc"]
            if len(field) < 3:
                field = field[1:]
            else:
                field = field[2:]

            msg = f"'{'.'.join(map(str, field))}': {message}"
    elif isinstance(exc, ValueError):
        error = exc.errors()[0]
        message = error["msg"]
        msg = message.split(",")[1].strip()
    else:
        msg = exc

    response.message = msg
    return JSONResponse(content=jsonable_encoder(response), status_code=status)


def validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    return _prepare_response(status=400, exc=exc)


def value_error_handler(_: Request, exc: ValueError) -> JSONResponse:
    return _prepare_response(status=422, exc=exc)


def custom_error_handler(_: Request, exc: CustomException) -> JSONResponse:
    return _prepare_response(status=exc.status, exc=exc.message)