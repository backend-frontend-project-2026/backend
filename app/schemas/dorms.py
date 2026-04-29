from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    IDSchema,
    PaginatedResponse,
)


class DormCreate(BaseModel):
    name: str = Field(max_length=255)
    city: str
    address: str = Field(max_length=255)


class DormUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
    city: Optional[str] = None
    address: Optional[str] = Field(default=None, max_length=255)


class DormPublic(IDSchema):
    uni_id: int
    name: str
    city: str
    address: str


class DormResponse(ApiResponseModel, DormPublic):
    pass


class DormListResponse(PaginatedResponse[DormResponse]):
    pass


class DormFilters(CommonListFilters):
    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = None
    city: Optional[str] = None
    uni_id: Optional[int] = Field(default=None, alias='university_id')
