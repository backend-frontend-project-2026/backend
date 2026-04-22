from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import ApiResponseModel, CommonListFilters


class DealType(str, Enum):
    RENT = 'rent'
    DORM = 'dorm'


class DealCreate(BaseModel):
    owner_profile_id: int
    title: str = Field(max_length=120)
    deal_type: DealType
    city: str
    neighbourhood_id: Optional[int] = None
    budget_min: Optional[int] = None
    budget_max: int
    people_amount: int = Field(ge=1)
    dorm_id: Optional[int] = None


class DealUpdate(BaseModel):
    owner_profile_id: Optional[int] = None
    title: Optional[str] = Field(default=None, max_length=120)
    deal_type: Optional[DealType] = None
    city: Optional[str] = None
    neighbourhood_id: Optional[int] = None
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    people_amount: Optional[int] = Field(default=None, ge=1)
    dorm_id: Optional[int] = None


class DealResponse(ApiResponseModel):
    id: int
    owner_profile_id: int
    title: str
    deal_type: DealType
    city: str
    neighbourhood_id: Optional[int]
    budget_min: Optional[int]
    budget_max: int
    people_amount: int
    dorm_id: Optional[int]
    created_at: datetime


class DealListResponse(ApiResponseModel):
    items: list[DealResponse]
    total: int
    page: int
    page_size: int


class DealFilters(CommonListFilters):
    city: Optional[str] = None
    deal_type: Optional[DealType] = None
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    people_amount: Optional[int] = None
    neighbourhood_id: Optional[int] = None
