from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel
from app.schemas.base import CreatedAtSchema, IDSchema

if TYPE_CHECKING:
    from app.models.deals import DealModel
    from app.models.messages import MessageModel
    from app.models.profiles import ProfileModel


class ChatBase(SQLModel):
    profile_id: int = Field(foreign_key='profiles.id')
    deal_id: int = Field(foreign_key='deals.id')


class ChatCreate(ChatBase):
    pass


class ChatUpdate(SQLModel):
    profile_id: Optional[int] = None
    deal_id: Optional[int] = None


class ChatPublic(ChatBase, IDSchema, CreatedAtSchema):
    pass


class ChatModel(ChatBase, IDModel, TimestampedModel, table=True):
    __tablename__ = 'chats'

    profile: Optional['ProfileModel'] = Relationship(back_populates='chats')
    deal: Optional['DealModel'] = Relationship(back_populates='chats')

    messages: list['MessageModel'] = Relationship(
        back_populates='chat',
        sa_relationship_kwargs={
            'lazy': 'selectin',
            'cascade': 'all, delete-orphan',
        },
    )