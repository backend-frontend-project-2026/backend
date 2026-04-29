from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.deals import DealModel
    from app.models.universities import UniversityModel

class DormModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'dorms'

    uni_id: int = Field(foreign_key='universities.id')
    name: str = Field(max_length=255)
    city: str
    address: str = Field(max_length=255)

    university: Optional['UniversityModel'] = Relationship(back_populates='dorms')
    deals: list['DealModel'] = Relationship(back_populates='dorm')
