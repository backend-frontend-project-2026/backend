from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    IDSchema,
    PaginatedResponse,
)


class FacultyCreate(BaseModel):
    name: str = Field(max_length=255)


class FacultyUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)


class FacultyPublic(IDSchema):
    uni_id: int
    name: str


class FacultyResponse(ApiResponseModel, FacultyPublic):
    pass


class FacultyListResponse(PaginatedResponse[FacultyResponse]):
    pass


class FacultyFilters(CommonListFilters):
    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = None
    uni_id: Optional[int] = Field(default=None, alias='university_id')
