from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel as SchemaModel
from pydantic import Field as SchemaField
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel
from app.schemas.base import IDSchema

if TYPE_CHECKING:
    from app.models.profiles import ProfileModel


class TagCategory(str, Enum):
    SLEEP_SCHEDULE = 'sleep_schedule'
    CLEANLINESS = 'cleanliness'
    NOISE_LEVEL = 'noise_level'
    GUEST_FREQUENCY = 'guest_frequency'
    SMOKING_PREFERENCE = 'smoking_preference'
    ALCOHOL_PREFERENCE = 'alcohol_preference'
    ROOM_ORDER_PREFERENCE = 'room_order_preference'
    PET_PREFERENCE = 'pet_preference'
    INTERESTS = 'interests'


class ProfileTagLink(SQLModel, table=True):
    __tablename__ = 'profile_tag_links'

    profile_id: int = Field(foreign_key='profiles.id', primary_key=True)
    tag_id: int = Field(foreign_key='tags.id', primary_key=True)


class TagBase(SchemaModel):
    category: TagCategory
    value: str = SchemaField(max_length=100)
    label: str = SchemaField(max_length=255)


class TagCreate(TagBase):
    pass


class TagUpdate(SchemaModel):
    category: Optional[TagCategory] = None
    value: Optional[str] = SchemaField(default=None, max_length=100)
    label: Optional[str] = SchemaField(default=None, max_length=255)


class TagPublic(TagBase, IDSchema):
    pass


class TagModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'tags'

    category: TagCategory
    value: str = Field(max_length=100)
    label: str = Field(max_length=255)

    profiles: list['ProfileModel'] = Relationship(
        back_populates='tags',
        link_model=ProfileTagLink,
    )