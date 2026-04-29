from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.complaints import (
    ComplaintReason,
    ComplaintStatus,
)
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    CreatedAtSchema,
    IDSchema,
    PaginatedResponse,
)


class ComplaintBase(BaseModel):
    complainant_id: int
    reported_user_id: int
    reason: ComplaintReason
    screenshots: Optional[str] = None


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintUpdate(BaseModel):
    status: Optional[ComplaintStatus] = None


class ComplaintPublic(ComplaintBase, IDSchema, CreatedAtSchema):
    status: ComplaintStatus


class ComplaintResponse(ApiResponseModel, ComplaintPublic):
    pass


class ComplaintListResponse(PaginatedResponse[ComplaintResponse]):
    pass


class ComplaintFilters(CommonListFilters):
    complainant_id: Optional[int] = None
    reported_user_id: Optional[int] = None
    status: Optional[ComplaintStatus] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
