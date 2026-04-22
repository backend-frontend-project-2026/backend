from enum import Enum
from typing import Optional

from sqlmodel import Field

from app.models.base import BaseModel


class DealType(str, Enum):
    RENT = 'rent'
    DORM = 'dorm'


class DealModel(BaseModel, table=True):
    __tablename__ = 'deals'

    owner_profile_id: int = Field(foreign_key='profiles.id')
    title: str = Field(max_length=120)
    deal_type: DealType
    city: str
    neighbourhood_id: Optional[int] = Field(
        default=None,
        foreign_key='neighbourhoods.id',
    )
    budget_min: Optional[int] = Field(default=None)
    budget_max: int
    people_amount: int
    dorm_id: Optional[int] = Field(default=None, foreign_key='dorms.id')
