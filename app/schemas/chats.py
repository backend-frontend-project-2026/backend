from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    CreatedAtSchema,
    IDSchema,
    PaginatedResponse,
)


class ChatBase(BaseModel):
    profile_id: int
    deal_id: int


class ChatCreate(ChatBase):
    pass


class ChatUpdate(BaseModel):
    profile_id: Optional[int] = None
    deal_id: Optional[int] = None


class ChatPublic(ChatBase, IDSchema, CreatedAtSchema):
    pass


class ChatResponse(ApiResponseModel, ChatPublic):
    pass


class ChatListResponse(PaginatedResponse[ChatResponse]):
    pass


class ChatFilters(CommonListFilters):
    profile_id: Optional[int] = None
    deal_id: Optional[int] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
