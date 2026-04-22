from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.schemas.base import ApiResponseModel, CommonListFilters


class ReactionType(str, Enum):
    LIKE = 'like'
    DISLIKE = 'dislike'


class ReactionCreate(BaseModel):
    profile_id: int
    reaction_type: ReactionType


class ReactionResponse(ApiResponseModel):
    id: int
    deal_id: int
    profile_id: int
    reaction_type: ReactionType
    created_at: datetime


class ReactionListResponse(ApiResponseModel):
    items: list[ReactionResponse]
    total: int
    page: int
    page_size: int


class ReactionFilters(CommonListFilters):
    deal_id: Optional[int] = None
    reaction_type: Optional[ReactionType] = None
    profile_id: Optional[int] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
