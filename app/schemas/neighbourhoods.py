from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    IDSchema,
    PaginatedResponse,
)


class NeighbourhoodBase(BaseModel):
    city: str = Field(max_length=100)
    district_name: str = Field(max_length=100)


class NeighbourhoodCreate(NeighbourhoodBase):
    pass


class NeighbourhoodUpdate(BaseModel):
    city: Optional[str] = Field(default=None, max_length=100)
    district_name: Optional[str] = Field(default=None, max_length=100)


class NeighbourhoodPublic(NeighbourhoodBase, IDSchema):
    pass


class NeighbourhoodResponse(ApiResponseModel, NeighbourhoodPublic):
    pass


class NeighbourhoodListResponse(PaginatedResponse[NeighbourhoodResponse]):
    pass


class NeighbourhoodFilters(CommonListFilters):
    district_name: Optional[str] = None
    city: Optional[str] = None
