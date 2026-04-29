from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    IDSchema,
    PaginatedResponse,
)


class MessageCreate(BaseModel):
    profile_id: int
    content: str = Field(max_length=1000)


class MessageUpdate(BaseModel):
    content: Optional[str] = Field(default=None, max_length=1000)
    is_read: Optional[bool] = None


class MessagePublic(IDSchema):
    chat_id: int
    profile_id: int
    content: str
    is_read: bool
    sent_at: datetime


class MessageResponse(ApiResponseModel, MessagePublic):
    pass


class MessageListResponse(PaginatedResponse[MessageResponse]):
    pass


class ChatMessageFilters(CommonListFilters):
    profile_id: Optional[int] = None
    sent_from: Optional[datetime] = None
    sent_to: Optional[datetime] = None
    is_read: Optional[bool] = None


class MessageFilters(ChatMessageFilters):
    chat_id: Optional[int] = None
