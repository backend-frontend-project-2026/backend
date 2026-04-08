from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.chats import ChatModel
    from app.models.profiles import ProfileModel


class MessageBase(TimestampedModel):
    content: str


class MessageCreate(SQLModel):
    chat_id: int
    profile_id: int
    content: str


class MessageUpdate(SQLModel):
    content: Optional[str] = None
    opened_at: Optional[datetime] = None


class MessagePublic(MessageBase, IDModel):
    chat_id: int
    profile_id: int
    opened_at: Optional[datetime] = None


class MessageModel(MessageBase, IDModel, table=True):
    __tablename__ = 'messages'

    chat_id: int = Field(foreign_key='chats.id')
    profile_id: int = Field(foreign_key='profiles.id')
    opened_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )

    chat: 'ChatModel' = Relationship(back_populates='messages')