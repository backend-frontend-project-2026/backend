from datetime import datetime
from typing import Optional

from app.models.complaints import (
    ComplaintPublic,
    ComplaintStatus,
)
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    PaginatedResponse,
)


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
