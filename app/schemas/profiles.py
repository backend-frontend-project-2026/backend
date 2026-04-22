from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.profiles import ProfileSex
from app.schemas.base import ApiResponseModel, CommonListFilters


class ProfileCreate(BaseModel):
    name: str
    sex: ProfileSex
    age: int = Field(ge=16)
    profile_description: Optional[str] = None
    uni_id: int
    faculty_id: int
    course: Optional[int] = Field(default=None, ge=1)
    city: str
    neighbourhood_id: Optional[int] = None


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    sex: Optional[ProfileSex] = None
    age: Optional[int] = Field(default=None, ge=16)
    profile_description: Optional[str] = None
    uni_id: Optional[int] = None
    faculty_id: Optional[int] = None
    course: Optional[int] = Field(default=None, ge=1)
    city: Optional[str] = None
    neighbourhood_id: Optional[int] = None


class ProfileResponse(ApiResponseModel):
    id: int
    user_id: int
    name: str
    sex: ProfileSex
    age: int
    profile_description: Optional[str]
    uni_id: int
    faculty_id: int
    course: Optional[int]
    city: str
    neighbourhood_id: Optional[int]
    created_at: datetime


class ProfileListResponse(ApiResponseModel):
    items: list[ProfileResponse]
    total: int
    page: int
    page_size: int


class ProfileFilters(CommonListFilters):
    user_id: Optional[int] = None
    sex: Optional[ProfileSex] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    uni_id: Optional[int] = None
    faculty_id: Optional[int] = None
    city: Optional[str] = None
    neighbourhood_id: Optional[int] = None
    tag_id: Optional[int] = None
    course: Optional[int] = None
