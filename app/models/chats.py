from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.profiles import ProfileModel
    from app.models.messages import MessageModel


class ChatModel(BaseModel, table=True):
    profile_id: int = Field(foreign_key='ProfileModel.id')
    deal_id: int = Field(foreign_key='DealModel.id')

    messages: List['MessageModel'] = Relationship(
        sa_relationship_kwargs={
            'lazy': 'selectin',
            'foreign_keys': '[MessageModel.profile_id]'
        },
    )
