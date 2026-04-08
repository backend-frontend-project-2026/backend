from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.dorms import DormModel
    from app.models.faculties import FacultyModel
    from app.models.profiles import ProfileModel


class UniversityBase(TimestampedModel):
    name: str = Field(unique=True, max_length=255)


class UniversityCreate(SQLModel):
    name: str = Field(max_length=255)


class UniversityUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=255)


class UniversityPublic(UniversityBase, IDModel):
    pass


class UniversityModel(UniversityBase, IDModel, table=True):
    __tablename__ = 'universities'

    faculties: list['FacultyModel'] = Relationship(
        back_populates='university',
        sa_relationship_kwargs={'lazy': 'selectin', 'cascade': 'all, delete-orphan'},
    )
    dorms: list['DormModel'] = Relationship(
        back_populates='university',
        sa_relationship_kwargs={'lazy': 'selectin', 'cascade': 'all, delete-orphan'},
    )
    profiles: list['ProfileModel'] = Relationship(back_populates='university')