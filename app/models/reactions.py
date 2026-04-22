from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, UniqueConstraint

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.profiles import ProfileModel


class ReactionType(str, Enum):
    LIKE = 'like'
    DISLIKE = 'dislike'


class ReactionModel(BaseModel, table=True):
    __tablename__ = 'reactions'

    reaction_type: ReactionType

    deal_id: int = Field(foreign_key='deals.id')
    profile_id: int = Field(foreign_key='profiles.id')

    profile: 'ProfileModel' = Relationship()

    __table_args__ = (
        UniqueConstraint('deal_id', 'profile_id', name='unique_reaction_pair'),
    )
