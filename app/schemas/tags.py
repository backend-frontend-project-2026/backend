from typing import Optional

from app.models.tags import TagCategory, TagPublic
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    PaginatedResponse,
)


class TagResponse(ApiResponseModel, TagPublic):
    pass


class TagListResponse(PaginatedResponse[TagResponse]):
    pass


class TagFilters(CommonListFilters):
    category: Optional[TagCategory] = None
    value: Optional[str] = None
