from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.base import ApiResponseModel, CommonListFilters


class ChatCreate(BaseModel):
    profile_id: int
    deal_id: int


class ChatUpdate(BaseModel):
    profile_id: int | None = None
    deal_id: int | None = None


class ChatResponse(ApiResponseModel):
    id: int
    profile_id: int
    deal_id: int
    created_at: datetime


class ChatListResponse(ApiResponseModel):
    items: list[ChatResponse]
    total: int
    page: int
    page_size: int


class ChatFilters(CommonListFilters):
    profile_id: Optional[int] = None
    deal_id: Optional[int] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
