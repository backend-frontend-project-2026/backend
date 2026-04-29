from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.deals import DealModel
    from app.models.profiles import ProfileModel


class ReactionType(str, Enum):
    LIKE = 'like'
    DISLIKE = 'dislike'

class ReactionModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'reactions'
    __table_args__ = (
        UniqueConstraint('profile_id', 'deal_id', name='unique_profile_deal_reaction'),
    )

    profile_id: int = Field(foreign_key='profiles.id')
    reaction_type: ReactionType
    deal_id: int = Field(foreign_key='deals.id')

    profile: Optional['ProfileModel'] = Relationship(back_populates='sent_reactions')
    deal: Optional['DealModel'] = Relationship(back_populates='reactions')
