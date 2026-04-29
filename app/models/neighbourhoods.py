from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.deals import DealModel
    from app.models.profiles import ProfileModel

class NeighbourhoodModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'neighbourhoods'

    city: str = Field(max_length=100)
    district_name: str = Field(max_length=100)

    profiles: list['ProfileModel'] = Relationship(back_populates='neighbourhood')
    deals: list['DealModel'] = Relationship(back_populates='neighbourhood')
