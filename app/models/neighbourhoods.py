from typing import TYPE_CHECKING

from pydantic import BaseModel as SchemaModel
from pydantic import Field as SchemaField
from sqlmodel import Field, Relationship

from app.models.base import IDModel, TimestampedModel
from app.schemas.base import IDSchema

if TYPE_CHECKING:
    from app.models.deals import DealModel
    from app.models.profiles import ProfileModel


class NeighbourhoodBase(SchemaModel):
    city: str = SchemaField(max_length=100)
    district_name: str = SchemaField(max_length=100)


class NeighbourhoodCreate(NeighbourhoodBase):
    pass


class NeighbourhoodUpdate(SchemaModel):
    city: str | None = SchemaField(default=None, max_length=100)
    district_name: str | None = SchemaField(default=None, max_length=100)


class NeighbourhoodPublic(NeighbourhoodBase, IDSchema):
    pass


class NeighbourhoodModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'neighbourhoods'

    city: str = Field(max_length=100)
    district_name: str = Field(max_length=100)

    profiles: list['ProfileModel'] = Relationship(back_populates='neighbourhood')
    deals: list['DealModel'] = Relationship(back_populates='neighbourhood')
