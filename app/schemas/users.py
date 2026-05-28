from typing import Optional

from app.models.users import UserPublic
from app.schemas.base import (
    CommonListFilters,
    PaginatedResponse,
)


class UserListResponse(PaginatedResponse[UserPublic]):
    pass


class UserFilters(CommonListFilters):
    email: Optional[str] = None

