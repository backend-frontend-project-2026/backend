from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.deals import DealModel
    from app.models.universities import UniversityModel


class DormBase(TimestampedModel):
    name: str = Field(max_length=255)
    address: str = Field(max_length=255)


class DormCreate(SQLModel):
    uni_id: int
    name: str = Field(max_length=255)
    address: str = Field(max_length=255)


class DormUpdate(SQLModel):
    uni_id: Optional[int] = None
    name: Optional[str] = Field(default=None, max_length=255)
    address: Optional[str] = Field(default=None, max_length=255)


class DormPublic(DormBase, IDModel):
    uni_id: int


class DormModel(DormBase, IDModel, table=True):
    __tablename__ = 'dorms'

    uni_id: int = Field(foreign_key='universities.id')

    university: Optional['UniversityModel'] = Relationship(back_populates='dorms')
    deals: list['DealModel'] = Relationship(back_populates='dorm')