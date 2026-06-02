from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import logger
from app.exceptions.base import AppError
from app.schemas.errors import ErrorResponse


def build_error_response(message: str, details: dict | None = None) -> dict:
    return ErrorResponse(
        message=message,
        details={
            'optional': details or {},
        },
    ).model_dump()


async def app_error_handler(
    request: Request,
    exc: AppError,
) -> JSONResponse:
    logger.warning(
        'Application error: method=%s path=%s status=%s message=%s',
        request.method,
        request.url.path,
        exc.status_code,
        exc.message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=build_error_response(
            message=exc.message,
            details=exc.details,
        ),
    )


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    logger.warning(
        'HTTP error: method=%s path=%s status=%s detail=%s',
        request.method,
        request.url.path,
        exc.status_code,
        exc.detail,
    )

    message = str(exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content=build_error_response(message=message),
        headers=exc.headers,
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    logger.warning(
        'Validation error: method=%s path=%s errors=%s',
        request.method,
        request.url.path,
        exc.errors(),
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=build_error_response(
            message='Validation error',
            details={'errors': exc.errors()},
        ),
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        'Unhandled error: method=%s path=%s',
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=build_error_response(message='Internal server error'),
    )