from pydantic import BaseModel

from app.schemas.base import ApiResponseModel, CommonListFilters


class NeighbourhoodCreate(BaseModel):
    district_name: str
    city: str


class NeighbourhoodUpdate(BaseModel):
    district_name: str | None = None
    city: str | None = None


class NeighbourhoodResponse(ApiResponseModel):
    id: int
    district_name: str
    city: str


class NeighbourhoodListResponse(ApiResponseModel):
    items: list[NeighbourhoodResponse]
    total: int
    page: int
    page_size: int


class NeighbourhoodFilters(CommonListFilters):
    district_name: str | None = None
    city: str | None = None
