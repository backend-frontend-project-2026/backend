from typing import Optional

from pydantic import ConfigDict, Field

from app.models.faculties import FacultyPublic
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    PaginatedResponse,
)


class FacultyResponse(ApiResponseModel, FacultyPublic):
    pass


class FacultyListResponse(PaginatedResponse[FacultyResponse]):
    pass


class FacultyFilters(CommonListFilters):
    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = None
    uni_id: Optional[int] = Field(default=None, alias='university_id')
