from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.universities import UniversityModel

class FacultyModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'faculties'

    uni_id: int = Field(foreign_key='universities.id')
    name: str = Field(max_length=255)

    university: Optional['UniversityModel'] = Relationship(back_populates='faculties')
