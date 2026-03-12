from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.likes import LikeModel
    from app.models.neighbourhoods import Neighbourhood
    from app.models.dorms import DormModel


class DealType(str, Enum):
    pass # придумать надо


class DealModel(BaseModel, table=True):
    like_id: int = Field(foreign_key="LikeModel.id")
    title: str
    deal_type: DealType
    city: str
    neighbourhood_id: int = Field(foreign_key="Neighbourhood.id")
    budget_min: int
    budget_max: int
    people_amount: int
    dorm_id: int = Field(foreign_key="DormModel.id")
