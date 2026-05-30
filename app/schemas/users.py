from typing import Any, Optional

from pydantic import field_validator

from app.models.users import UserPublic, UserStatus
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    PaginatedResponse,
)


class UserResponse(ApiResponseModel, UserPublic):
    @field_validator('roles', mode='before')
    @classmethod
    def extract_role_names(cls, v: Any) -> list[str]:
        if not v:
            return []
        if v and hasattr(v[0], 'name'):
            return [role.name for role in v]
        return list(v)


class UserListResponse(PaginatedResponse[UserResponse]):
    pass


class UserFilters(CommonListFilters):
    email: Optional[str] = None
    status: Optional[UserStatus] = None
