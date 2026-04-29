from typing import Optional

from pydantic import BaseModel, Field

from app.models.profiles import (
    ProfileSex,
)
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    CreatedAtSchema,
    IDSchema,
    PaginatedResponse,
)


class ProfileBase(BaseModel):
    uni_id: int
    faculty_id: int
    name: str = Field(max_length=50)
    sex: ProfileSex
    age: int = Field(ge=16)
    profile_description: Optional[str] = None
    course: Optional[int] = Field(default=None, ge=1)
    city: str
    neighbourhood_id: Optional[int] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    uni_id: Optional[int] = None
    faculty_id: Optional[int] = None
    name: Optional[str] = Field(default=None, max_length=50)
    sex: Optional[ProfileSex] = None
    age: Optional[int] = Field(default=None, ge=16)
    profile_description: Optional[str] = None
    course: Optional[int] = Field(default=None, ge=1)
    city: Optional[str] = None
    neighbourhood_id: Optional[int] = None


class ProfilePublic(ProfileBase, IDSchema, CreatedAtSchema):
    user_id: int


class ProfileResponse(ApiResponseModel, ProfilePublic):
    pass


class ProfileListResponse(PaginatedResponse[ProfileResponse]):
    pass


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
