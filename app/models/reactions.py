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

    profile_id: int = Field(foreign_key='profiles.id')
    target_profile_id: int = Field(foreign_key='profiles.id')

    profile: 'ProfileModel' = Relationship(back_populates='sent_reactions')
    target_profile: 'ProfileModel' = Relationship(back_populates='received_reactions')

    __table_args__ = (
        UniqueConstraint(
            'profile_id', 'target_profile_id', name='unique_reaction_pair'
        ),
    )
