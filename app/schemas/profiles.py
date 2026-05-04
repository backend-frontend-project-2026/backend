from typing import Optional

from app.models.profiles import (
    ProfilePublic,
    ProfileSex,
)
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    PaginatedResponse,
)


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
