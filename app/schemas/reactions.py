from datetime import datetime
from typing import Optional

from app.models.reactions import ReactionPublic, ReactionType
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    PaginatedResponse,
)


class ReactionResponse(ApiResponseModel, ReactionPublic):
    pass


class ReactionListResponse(PaginatedResponse[ReactionResponse]):
    pass


class ReactionFilters(CommonListFilters):
    deal_id: Optional[int] = None
    reaction_type: Optional[ReactionType] = None
    profile_id: Optional[int] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
