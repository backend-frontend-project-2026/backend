from datetime import datetime
from datetime import timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.chats import ChatModel


class MessageBase(TimestampedModel):
    chat_id: int = Field(foreign_key='chats.id')
    profile_id: int = Field(foreign_key='profiles.id')
    content: str = Field(max_length=1000)
    is_read: bool = Field(default=False)
    sent_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )


class MessageCreate(MessageBase):
    pass


class MessageUpdate(SQLModel):
    content: Optional[str] = Field(default=None, max_length=1000)
    is_read: Optional[bool] = None


class MessagePublic(MessageBase, IDModel):
    pass


class MessageModel(MessageBase, IDModel, table=True):
    __tablename__ = 'messages'

    chat: Optional['ChatModel'] = Relationship(back_populates='messages')
