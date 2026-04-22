from pydantic import BaseModel

from app.schemas.base import ApiResponseModel, CommonListFilters


class TagCreate(BaseModel):
    category: str
    value: str


class TagUpdate(BaseModel):
    category: str | None = None
    value: str | None = None


class TagResponse(ApiResponseModel):
    id: int
    category: str
    value: str


class TagListResponse(ApiResponseModel):
    items: list[TagResponse]
    total: int
    page: int
    page_size: int


class TagFilters(CommonListFilters):
    category: str | None = None
    value: str | None = None
