from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.deals import DealModel
    from app.models.messages import MessageModel
    from app.models.profiles import ProfileModel

class ChatModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'chats'

    profile_id: int = Field(foreign_key='profiles.id')
    deal_id: int = Field(foreign_key='deals.id')

    profile: Optional['ProfileModel'] = Relationship(back_populates='chats')
    deal: Optional['DealModel'] = Relationship(back_populates='chats')

    messages: list['MessageModel'] = Relationship(
        back_populates='chat',
        sa_relationship_kwargs={
            'lazy': 'selectin',
            'cascade': 'all, delete-orphan',
        },
    )
