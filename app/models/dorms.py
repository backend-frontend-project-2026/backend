from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.universities import UniversityModel


class DormModel(BaseModel, table=True):
    uni_id: int = Field(foreign_key='UniversityModel.id')

    university: Optional['UniversityModel'] = Relationship(back_populates="dorms")
