from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.deals import DealModel
    from app.models.profiles import ProfileModel


class ReactionType(str, Enum):
    LIKE = 'like'
    DISLIKE = 'dislike'


class ReactionBase(TimestampedModel):
    reaction_type: ReactionType


class ReactionCreate(SQLModel):
    profile_id: int
    deal_id: int
    reaction_type: ReactionType


class ReactionUpdate(SQLModel):
    reaction_type: Optional[ReactionType] = None


class ReactionPublic(ReactionBase, IDModel):
    profile_id: int
    deal_id: int


class ReactionModel(ReactionBase, IDModel, table=True):
    __tablename__ = 'reactions'
    __table_args__ = (
        UniqueConstraint('profile_id', 'deal_id', name='unique_profile_deal_reaction'),
    )

    profile_id: int = Field(foreign_key='profiles.id')
    deal_id: int = Field(foreign_key='deals.id')

    profile: 'ProfileModel' = Relationship(back_populates='sent_reactions')
    deal: 'DealModel' = Relationship(back_populates='reactions')