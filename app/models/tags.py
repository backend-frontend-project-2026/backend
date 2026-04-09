from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.profiles import ProfileModel


class TagCategory(str, Enum):
    NOISE = 'noise'
    BAD_HABITS = 'bad_habits'
    GUESTS = 'guests'
    CLEANLINESS = 'cleanliness'
    ROOM_ORDER = 'room_order'
    SLEEP_SCHEDULE = 'sleep_schedule'


class ProfileTagLink(SQLModel, table=True):
    __tablename__ = 'profile_tag_links'

    profile_id: int = Field(foreign_key='profiles.id', primary_key=True)
    tag_id: int = Field(foreign_key='tags.id', primary_key=True)


class TagBase(TimestampedModel):
    category: TagCategory
    value: str = Field(max_length=100)


class TagCreate(TagBase):
    pass


class TagUpdate(SQLModel):
    category: Optional[TagCategory] = None
    value: Optional[str] = Field(default=None, max_length=100)


class TagPublic(TagBase, IDModel):
    pass


class TagModel(TagBase, IDModel, table=True):
    __tablename__ = 'tags'

    profiles: list['ProfileModel'] = Relationship(
        back_populates='tags',
        link_model=ProfileTagLink,
    )