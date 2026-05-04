from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel as SchemaModel
from pydantic import Field as SchemaField
from sqlmodel import Field, Relationship

from app.models.base import IDModel, TimestampedModel
from app.schemas.base import IDSchema

if TYPE_CHECKING:
    from app.models.universities import UniversityModel


class FacultyBase(SchemaModel):
    name: str = SchemaField(max_length=255)


class FacultyCreate(FacultyBase):
    pass


class FacultyUpdate(SchemaModel):
    name: Optional[str] = SchemaField(default=None, max_length=255)


class FacultyPublic(FacultyBase, IDSchema):
    uni_id: int


class FacultyModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'faculties'

    uni_id: int = Field(foreign_key='universities.id')
    name: str = Field(max_length=255)

    university: Optional['UniversityModel'] = Relationship(back_populates='faculties')
