from typing import Optional

from app.models.universities import UniversityPublic
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    PaginatedResponse,
)


class UniversityResponse(ApiResponseModel, UniversityPublic):
    pass


class UniversityListResponse(PaginatedResponse[UniversityResponse]):
    pass


class UniversityFilters(CommonListFilters):
    name: Optional[str] = None
    city: Optional[str] = None
