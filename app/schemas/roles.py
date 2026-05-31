from typing import Optional

from pydantic import BaseModel

from app.schemas.base import ApiResponseModel, CommonListFilters, IDSchema, PaginatedResponse


class PermissionPublic(IDSchema):
    scope: str


class PermissionResponse(ApiResponseModel, PermissionPublic):
    pass


class PermissionListResponse(PaginatedResponse[PermissionResponse]):
    pass


class PermissionFilters(CommonListFilters):
    scope: Optional[str] = None


class RolePublic(IDSchema):
    name: str
    scopes: list[str]


class RoleResponse(ApiResponseModel, RolePublic):
    pass


class RoleListResponse(PaginatedResponse[RoleResponse]):
    pass


class RoleFilters(CommonListFilters):
    name: Optional[str] = None


class RoleCreate(BaseModel):
    name: str
    scope_aliases: list[str] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    scope_aliases: Optional[list[str]] = None
