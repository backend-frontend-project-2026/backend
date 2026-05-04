from typing import Optional

from app.models.neighbourhoods import NeighbourhoodPublic
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    PaginatedResponse,
)


class NeighbourhoodResponse(ApiResponseModel, NeighbourhoodPublic):
    pass


class NeighbourhoodListResponse(PaginatedResponse[NeighbourhoodResponse]):
    pass


class NeighbourhoodFilters(CommonListFilters):
    district_name: Optional[str] = None
    city: Optional[str] = None
