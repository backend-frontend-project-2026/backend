from typing import Optional

from pydantic import ConfigDict, Field

from app.models.dorms import DormPublic
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    PaginatedResponse,
)


class DormResponse(ApiResponseModel, DormPublic):
    pass


class DormListResponse(PaginatedResponse[DormResponse]):
    pass


class DormFilters(CommonListFilters):
    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = None
    city: Optional[str] = None
    uni_id: Optional[int] = Field(default=None, alias='university_id')
