from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status
from starlette.requests import Request

from project.app.infrastructure.errors.base import BaseError
from project.app.infrastructure.models import ErrorResponse, ErrorResponseMulti


def custom_base_errors_handler(_: Request, error: BaseError) -> JSONResponse:
    """This function is called if the BaseError was raised."""

    response = ErrorResponseMulti(
        results=[ErrorResponse(message=error.message.capitalize())]
    )

    return JSONResponse(
        response.dict(by_alias=True),
        status_code=error.status_code,
    )


def python_base_error_handler(_: Request, error: Exception) -> JSONResponse:
    """This function is called if the Exception was raised."""

    response = ErrorResponseMulti(
        results=[ErrorResponse(message=f"Unhandled error: {error}")]
    )

    return JSONResponse(
        content=jsonable_encoder(response.dict(by_alias=True)),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def pydantic_validation_errors_handler(
    _: Request, error: RequestValidationError
) -> JSONResponse:
    """This function is called if the Pydantic validation error was raised."""

    response = ErrorResponseMulti(
        results=[
            ErrorResponse(
                message=err["msg"],
                path=list(err["loc"]),
            )
            for err in error.errors()
        ]
    )

    return JSONResponse(
        content=jsonable_encoder(response.dict(by_alias=True)),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
