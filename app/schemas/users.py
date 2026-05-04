from typing import Optional

from app.models.users import UserPublic, UserRole
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    PaginatedResponse,
)


class UserResponse(ApiResponseModel, UserPublic):
    pass


class UserListResponse(PaginatedResponse[UserResponse]):
    pass


class UserFilters(CommonListFilters):
    email: Optional[str] = None
    role: Optional[UserRole] = None
