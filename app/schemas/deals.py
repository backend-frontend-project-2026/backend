from typing import Optional

from pydantic import BaseModel, Field

from app.models.deals import DealType
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    CreatedAtSchema,
    IDSchema,
    PaginatedResponse,
)


class DealBase(BaseModel):
    owner_profile_id: int
    title: str = Field(max_length=120)
    deal_type: DealType
    city: str
    neighbourhood_id: Optional[int] = None
    dorm_id: Optional[int] = None
    budget_min: Optional[int] = None
    budget_max: int
    people_amount: int = Field(ge=1)


class DealCreate(DealBase):
    pass


class DealUpdate(BaseModel):
    owner_profile_id: Optional[int] = None
    neighbourhood_id: Optional[int] = None
    dorm_id: Optional[int] = None
    title: Optional[str] = Field(default=None, max_length=120)
    deal_type: Optional[DealType] = None
    city: Optional[str] = None
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    people_amount: Optional[int] = Field(default=None, ge=1)


class DealPublic(DealBase, IDSchema, CreatedAtSchema):
    pass


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
