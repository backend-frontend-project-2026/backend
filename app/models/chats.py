
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.messages import MessageModel

class ChatModel(BaseModel, table=True):
    __tablename__ = 'chats'

    profile_id: int = Field(foreign_key='profiles.id')
    deal_id: int = Field(foreign_key='deals.id')

    messages: list['MessageModel'] = Relationship(
        sa_relationship_kwargs={
            'lazy': 'selectin',
            'cascade': 'all, delete-orphan',
        },
    )
