from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.deals import DealModel
    from app.models.messages import MessageModel
    from app.models.profiles import ProfileModel


class ChatBase(TimestampedModel):
    pass


class ChatCreate(SQLModel):
    profile_id: int
    deal_id: int


class ChatUpdate(SQLModel):
    pass


class ChatPublic(ChatBase, IDModel):
    profile_id: int
    deal_id: int


class ChatModel(ChatBase, IDModel, table=True):
    __tablename__ = 'chats'

    profile_id: int = Field(foreign_key='profiles.id')
    deal_id: int = Field(foreign_key='deals.id')

    profile: 'ProfileModel' = Relationship(back_populates='chats')
    deal: 'DealModel' = Relationship(back_populates='chats')

    messages: list['MessageModel'] = Relationship(
        back_populates='chat',
        sa_relationship_kwargs={
            'lazy': 'selectin',
            'cascade': 'all, delete-orphan',
        },
    )