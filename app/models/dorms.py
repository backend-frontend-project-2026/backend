from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.deals import DealModel
    from app.models.universities import UniversityModel


class DormBase(TimestampedModel):
    uni_id: int = Field(foreign_key='universities.id')
    name: str = Field(max_length=255)
    address: str = Field(max_length=255)


class DormCreate(DormBase):
    pass


class DormUpdate(SQLModel):
    uni_id: Optional[int] = None
    name: Optional[str] = Field(default=None, max_length=255)
    address: Optional[str] = Field(default=None, max_length=255)


class DormPublic(DormBase, IDModel):
    pass


class DormModel(DormBase, IDModel, table=True):
    __tablename__ = 'dorms'

    university: Optional['UniversityModel'] = Relationship(back_populates='dorms')
    deals: list['DealModel'] = Relationship(back_populates='dorm')