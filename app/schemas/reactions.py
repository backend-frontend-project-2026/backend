from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.reactions import ReactionType
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    CreatedAtSchema,
    IDSchema,
    PaginatedResponse,
)


class ReactionBase(BaseModel):
    profile_id: int
    reaction_type: ReactionType


class ReactionCreate(ReactionBase):
    pass


class ReactionUpdate(BaseModel):
    reaction_type: Optional[ReactionType] = None


class ReactionPublic(ReactionBase, IDSchema, CreatedAtSchema):
    deal_id: int


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
