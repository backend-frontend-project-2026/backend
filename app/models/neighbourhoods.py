from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.deals import DealModel
    from app.models.profiles import ProfileModel


class NeighbourhoodBase(TimestampedModel):
    city: str = Field(max_length=100)
    district_name: str = Field(max_length=100)


class NeighbourhoodCreate(NeighbourhoodBase):
    pass


class NeighbourhoodUpdate(SQLModel):
    city: Optional[str] = Field(default=None, max_length=100)
    district_name: Optional[str] = Field(default=None, max_length=100)


class NeighbourhoodPublic(NeighbourhoodBase, IDModel):
    pass


class NeighbourhoodModel(NeighbourhoodBase, IDModel, table=True):
    __tablename__ = 'neighbourhoods'

    profiles: list['ProfileModel'] = Relationship(back_populates='neighbourhood')
    deals: list['DealModel'] = Relationship(back_populates='neighbourhood')