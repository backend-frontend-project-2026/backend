from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.users import UserRole
from app.schemas.base import ApiResponseModel, CommonListFilters


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    password: Optional[str] = Field(default=None, min_length=8)


class UserResponse(ApiResponseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: UserRole
    created_at: datetime


class UserListResponse(ApiResponseModel):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int


class UserFilters(CommonListFilters):
    email: Optional[str] = None
    role: Optional[UserRole] = None
