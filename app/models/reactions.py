from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel as SchemaModel
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship

from app.models.base import IDModel, TimestampedModel
from app.schemas.base import CreatedAtSchema, IDSchema

if TYPE_CHECKING:
    from app.models.deals import DealModel
    from app.models.profiles import ProfileModel


class ReactionType(str, Enum):
    LIKE = 'like'
    DISLIKE = 'dislike'


class ReactionBase(SchemaModel):
    profile_id: int
    reaction_type: ReactionType


class ReactionCreate(ReactionBase):
    pass


class ReactionUpdate(SchemaModel):
    reaction_type: Optional[ReactionType] = None


class ReactionPublic(ReactionBase, IDSchema, CreatedAtSchema):
    deal_id: int


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
