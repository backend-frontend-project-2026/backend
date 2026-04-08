from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.chats import ChatModel


class MessageModel(BaseModel, table=True):
    __tablename__ = 'messages'

    chat_id: int = Field(foreign_key='chats.id')
    profile_id: int = Field(foreign_key='profiles.id')
    content: str
    opened_at: Optional[datetime] = Field(
        default=None,
        sa_type=TIMESTAMP(timezone=True),
    )

    chat: 'ChatModel' = Relationship(back_populates='messages')
