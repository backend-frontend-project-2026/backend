from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import ApiResponseModel, CommonListFilters


class ComplaintStatus(str, Enum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    RESOLVED = 'resolved'
    REJECTED = 'rejected'


class ComplaintCreate(BaseModel):
    complainant_id: int
    reported_user_id: int
    reason: str = Field(max_length=1000)
    screenshots: Optional[str] = None


class ComplaintUpdate(BaseModel):
    status: Optional[ComplaintStatus] = None


class ComplaintResponse(ApiResponseModel):
    id: int
    complainant_id: int
    reported_user_id: int
    reason: str
    screenshots: Optional[str]
    status: ComplaintStatus
    created_at: datetime


class ComplaintListResponse(ApiResponseModel):
    items: list[ComplaintResponse]
    total: int
    page: int
    page_size: int


class ComplaintFilters(CommonListFilters):
    complainant_id: Optional[int] = None
    reported_user_id: Optional[int] = None
    status: Optional[ComplaintStatus] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
