from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.deals import DealModel
    from app.models.messages import MessageModel
    from app.models.profiles import ProfileModel


class ChatBase(TimestampedModel):
    profile_id: int = Field(foreign_key='profiles.id')
    deal_id: int = Field(foreign_key='deals.id')


class ChatCreate(ChatBase):
    pass


class ChatUpdate(SQLModel):
    profile_id: Optional[int] = None
    deal_id: Optional[int] = None


class ChatPublic(ChatBase, IDModel):
    pass


class ChatModel(ChatBase, IDModel, table=True):
    __tablename__ = 'chats'

    profile: 'ProfileModel' = Relationship(back_populates='chats')
    deal: 'DealModel' = Relationship(back_populates='chats')

    messages: list['MessageModel'] = Relationship(
        back_populates='chat',
        sa_relationship_kwargs={
            'lazy': 'selectin',
            'cascade': 'all, delete-orphan',
        },
    )