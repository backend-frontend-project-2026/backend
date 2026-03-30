from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.universities import UniversityModel


class DormModel(BaseModel, table=True):
    __tablename__ = 'dorms'

    uni_id: int = Field(foreign_key='universities.id')

    name: str
    address: str

    university: Optional['UniversityModel'] = Relationship(back_populates='dorms')
