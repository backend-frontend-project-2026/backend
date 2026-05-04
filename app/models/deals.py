from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel as SchemaModel
from pydantic import Field as SchemaField
from sqlmodel import Field, Relationship

from app.models.base import IDModel, TimestampedModel
from app.schemas.base import CreatedAtSchema, IDSchema

if TYPE_CHECKING:
    from app.models.chats import ChatModel
    from app.models.dorms import DormModel
    from app.models.neighbourhoods import NeighbourhoodModel
    from app.models.profiles import ProfileModel
    from app.models.reactions import ReactionModel


class DealType(str, Enum):
    RENT = 'rent'
    DORM = 'dorm'


class DealBase(SchemaModel):
    owner_profile_id: int
    title: str = SchemaField(max_length=120)
    deal_type: DealType
    city: str
    neighbourhood_id: Optional[int] = None
    dorm_id: Optional[int] = None
    budget_min: Optional[int] = None
    budget_max: int
    people_amount: int = SchemaField(ge=1)


class DealCreate(DealBase):
    pass


class DealUpdate(SchemaModel):
    owner_profile_id: Optional[int] = None
    neighbourhood_id: Optional[int] = None
    dorm_id: Optional[int] = None
    title: Optional[str] = SchemaField(default=None, max_length=120)
    deal_type: Optional[DealType] = None
    city: Optional[str] = None
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    people_amount: Optional[int] = SchemaField(default=None, ge=1)


class DealPublic(DealBase, IDSchema, CreatedAtSchema):
    pass


class DealModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'deals'

    owner_profile_id: int = Field(foreign_key='profiles.id')
    title: str = Field(max_length=120)
    deal_type: DealType
    city: str
    neighbourhood_id: Optional[int] = Field(
        default=None,
        foreign_key='neighbourhoods.id',
    )
    dorm_id: Optional[int] = Field(default=None, foreign_key='dorms.id')
    budget_min: Optional[int] = None
    budget_max: int
    people_amount: int = Field(ge=1)

    owner_profile: Optional['ProfileModel'] = Relationship(back_populates='deals')
    neighbourhood: Optional['NeighbourhoodModel'] = Relationship(back_populates='deals')
    dorm: Optional['DormModel'] = Relationship(back_populates='deals')
    reactions: list['ReactionModel'] = Relationship(back_populates='deal')
    chats: list['ChatModel'] = Relationship(back_populates='deal')
