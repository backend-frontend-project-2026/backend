class AppError(Exception):
    status_code: int = 500
    message: str = 'Internal server error'

    def __init__(
        self,
        message: str | None = None,
        details: dict | None = None,
    ):
        self.message = message or self.message
        self.details = details or {}
        super().__init__(self.message)


class BadRequestError(AppError):
    status_code = 400
    message = 'Bad request'


class UnauthorizedError(AppError):
    status_code = 401
    message = 'Unauthorized'


class ForbiddenError(AppError):
    status_code = 403
    message = 'Access denied'


class NotFoundError(AppError):
    status_code = 404
    message = 'Not found'


class ConflictError(AppError):
    status_code = 409
    message = 'Conflict'


class InternalServerError(AppError):
    status_code = 500
    message = 'Internal server error'