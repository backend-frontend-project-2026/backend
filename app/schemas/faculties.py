from pydantic import BaseModel

from app.schemas.base import ApiResponseModel, CommonListFilters


class FacultyCreate(BaseModel):
    uni_id: int
    name: str


class FacultyUpdate(BaseModel):
    uni_id: int | None = None
    name: str | None = None


class FacultyResponse(ApiResponseModel):
    id: int
    uni_id: int
    name: str


class FacultyListResponse(ApiResponseModel):
    items: list[FacultyResponse]
    total: int
    page: int
    page_size: int


class FacultyFilters(CommonListFilters):
    name: str | None = None
    uni_id: int | None = None
