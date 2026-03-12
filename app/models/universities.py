from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.dorms import DormModel


class UniversityModel(BaseModel, table=True):
    name: str = Field(unique=True)

    dorms: list['DormModel'] = Relationship(
        back_populates='university',
        sa_relationship_kwargs={'foreign_keys': 'DormModel.uni_id'}
    )
