from typing import Optional

from app.models.deals import DealPublic, DealType
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    PaginatedResponse,
)


class DealResponse(ApiResponseModel, DealPublic):
    pass


class DealListResponse(PaginatedResponse[DealResponse]):
    pass


class DealFilters(CommonListFilters):
    city: Optional[str] = None
    deal_type: Optional[DealType] = None
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    people_amount: Optional[int] = None
    neighbourhood_id: Optional[int] = None
