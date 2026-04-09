from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.universities import UniversityModel


class FacultyBase(TimestampedModel):
    uni_id: int = Field(foreign_key='universities.id')
    name: str = Field(max_length=255)


class FacultyCreate(FacultyBase):
    pass


class FacultyUpdate(SQLModel):
    uni_id: Optional[int] = None
    name: Optional[str] = Field(default=None, max_length=255)


class FacultyPublic(FacultyBase, IDModel):
    pass


class FacultyModel(FacultyBase, IDModel, table=True):
    __tablename__ = 'faculties'

    university: Optional['UniversityModel'] = Relationship(back_populates='faculties')