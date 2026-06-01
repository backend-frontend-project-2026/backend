from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.db.engine import async_session_maker
from app.exceptions.base import AppError
from app.exceptions.handlers import (
    app_error_handler,
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.middlewares.logging import RequestLoggingMiddleware
from app.routers.api import api_router
from app.services.bootstrap import bootstrap_roles_and_permissions


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session_maker() as session:
        await bootstrap_roles_and_permissions(session)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(RequestLoggingMiddleware)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(api_router)