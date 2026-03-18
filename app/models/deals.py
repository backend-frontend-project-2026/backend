from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.neighbourhoods import NeighbourhoodModel
    from app.models.dorms import DormModel


class DealStatus(str, Enum):
    PENDING = 'pending'
    DONE = 'done'
    CANCELLED = 'cancelled'


class DealModel(BaseModel, table=True):
    __tablename__ = 'deals'

    like_id: int = Field(foreign_key='reactions.id')
    neighbourhood_id: int = Field(foreign_key='neighbourhoods.id')
    dorm_id: Optional[int] = Field(foreign_key='dorms.id')

    title: str = Field(max_length=100)
    status: DealStatus = Field(default=DealStatus.PENDING)

    budget_min: int = Field()
    budget_max: int = Field()
    people_amount: int = Field()

    neighbourhood: Optional['NeighbourhoodModel'] = Relationship()
    dorm: Optional['DormModel'] = Relationship()
