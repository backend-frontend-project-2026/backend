from pydantic import BaseModel

from app.schemas.base import ApiResponseModel, CommonListFilters


class UniversityCreate(BaseModel):
    name: str
    city: str


class UniversityUpdate(BaseModel):
    name: str | None = None
    city: str | None = None


class UniversityResponse(ApiResponseModel):
    id: int
    name: str
    city: str


class UniversityListResponse(ApiResponseModel):
    items: list[UniversityResponse]
    total: int
    page: int
    page_size: int


class UniversityFilters(CommonListFilters):
    name: str | None = None
    city: str | None = None
