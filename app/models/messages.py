from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.chats import ChatModel

class MessageModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'messages'

    chat_id: int = Field(foreign_key='chats.id')
    profile_id: int = Field(foreign_key='profiles.id')
    content: str = Field(max_length=1000)
    is_read: bool = Field(default=False)
    sent_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    chat: Optional['ChatModel'] = Relationship(back_populates='messages')
