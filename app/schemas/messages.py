from datetime import datetime
from typing import Optional

from app.models.messages import MessagePublic
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    PaginatedResponse,
)


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
