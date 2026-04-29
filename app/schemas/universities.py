from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    IDSchema,
    PaginatedResponse,
)


class UniversityBase(BaseModel):
    name: str = Field(max_length=255)
    city: str


class UniversityCreate(UniversityBase):
    pass


class UniversityUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
    city: Optional[str] = None


class UniversityPublic(UniversityBase, IDSchema):
    pass


class UniversityResponse(ApiResponseModel, UniversityPublic):
    pass


class UniversityListResponse(PaginatedResponse[UniversityResponse]):
    pass


class UniversityFilters(CommonListFilters):
    name: Optional[str] = None
    city: Optional[str] = None
