from typing import Optional

from pydantic import BaseModel, Field

from app.models.tags import TagCategory
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    IDSchema,
    PaginatedResponse,
)


class TagBase(BaseModel):
    category: TagCategory
    value: str = Field(max_length=100)


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    category: Optional[TagCategory] = None
    value: Optional[str] = Field(default=None, max_length=100)


class TagPublic(TagBase, IDSchema):
    pass


class TagResponse(ApiResponseModel, TagPublic):
    pass


class TagListResponse(PaginatedResponse[TagResponse]):
    pass


class TagFilters(CommonListFilters):
    category: Optional[TagCategory] = None
    value: Optional[str] = None
