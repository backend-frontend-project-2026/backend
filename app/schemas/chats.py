from datetime import datetime
from typing import Optional

from app.models.chats import ChatPublic
from app.schemas.base import (
    ApiResponseModel,
    CommonListFilters,
    PaginatedResponse,
)


class ChatResponse(ApiResponseModel, ChatPublic):
    pass


class ChatListResponse(PaginatedResponse[ChatResponse]):
    pass


class ChatFilters(CommonListFilters):
    profile_id: Optional[int] = None
    deal_id: Optional[int] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
