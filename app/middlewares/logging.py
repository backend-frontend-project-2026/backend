import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        start_time = time.perf_counter()

        logger.info(
            'Request started: method=%s path=%s client=%s',
            request.method,
            request.url.path,
            request.client.host if request.client else None,
        )

        try:
            response = await call_next(request)
        except Exception:
            logger.exception(
                'Request failed: method=%s path=%s',
                request.method,
                request.url.path,
            )
            raise

        process_time = time.perf_counter() - start_time

        logger.info(
            'Request finished: method=%s path=%s status=%s duration=%.4fs',
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )

        return response