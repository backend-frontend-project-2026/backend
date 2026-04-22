from pydantic import BaseModel

from app.schemas.base import ApiResponseModel, CommonListFilters


class DormCreate(BaseModel):
    uni_id: int
    name: str
    city: str
    address: str


class DormUpdate(BaseModel):
    uni_id: int | None = None
    name: str | None = None
    city: str | None = None
    address: str | None = None


class DormResponse(ApiResponseModel):
    id: int
    uni_id: int
    name: str
    city: str
    address: str


class DormListResponse(ApiResponseModel):
    items: list[DormResponse]
    total: int
    page: int
    page_size: int


class DormFilters(CommonListFilters):
    name: str | None = None
    city: str | None = None
    uni_id: int | None = None
