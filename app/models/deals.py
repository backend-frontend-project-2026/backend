from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.chats import ChatModel
    from app.models.dorms import DormModel
    from app.models.neighbourhoods import NeighbourhoodModel
    from app.models.profiles import ProfileModel
    from app.models.reactions import ReactionModel


class DealStatus(str, Enum):
    ACTIVE = 'active'
    CLOSED = 'closed'
    CANCELLED = 'cancelled'


class DealType(str, Enum):
    RENT = 'rent'
    DORM = 'dorm'


class DealBase(TimestampedModel):
    owner_profile_id: int = Field(foreign_key='profiles.id')
    neighbourhood_id: int = Field(foreign_key='neighbourhoods.id')
    dorm_id: Optional[int] = Field(default=None, foreign_key='dorms.id')
    title: str = Field(max_length=100)
    deal_type: DealType
    status: DealStatus = Field(default=DealStatus.ACTIVE)
    budget_min: int
    budget_max: int
    people_amount: int


class DealCreate(DealBase):
    pass


class DealUpdate(SQLModel):
    neighbourhood_id: Optional[int] = None
    dorm_id: Optional[int] = None
    title: Optional[str] = Field(default=None, max_length=100)
    deal_type: Optional[DealType] = None
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    people_amount: Optional[int] = None
    status: Optional[DealStatus] = None


class DealPublic(DealBase, IDModel):
    pass


class DealModel(DealBase, IDModel, table=True):
    __tablename__ = 'deals'

    owner_profile: 'ProfileModel' = Relationship(back_populates='deals')
    neighbourhood: Optional['NeighbourhoodModel'] = Relationship(back_populates='deals')
    dorm: Optional['DormModel'] = Relationship(back_populates='deals')
    reactions: list['ReactionModel'] = Relationship(back_populates='deal')
    chats: list['ChatModel'] = Relationship(back_populates='deal')