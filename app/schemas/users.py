from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.users import UserRole
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    CreatedAtSchema,
    IDSchema,
    PaginatedResponse,
)


class UserBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)


class UserPublic(UserBase, IDSchema, CreatedAtSchema):
    pass


class UserResponse(ApiResponseModel, UserPublic):
    pass


class UserListResponse(PaginatedResponse[UserResponse]):
    pass


class UserFilters(CommonListFilters):
    email: Optional[str] = None
    role: Optional[UserRole] = None
