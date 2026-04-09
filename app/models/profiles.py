from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel
from app.models.tags import ProfileTagLink, TagModel

if TYPE_CHECKING:
    from app.models.chats import ChatModel
    from app.models.deals import DealModel
    from app.models.neighbourhoods import NeighbourhoodModel
    from app.models.reactions import ReactionModel
    from app.models.universities import UniversityModel
    from app.models.users import UserModel


class ProfileSex(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


class ProfileBase(TimestampedModel):
    user_id: int = Field(foreign_key='users.id', unique=True)
    uni_id: int = Field(foreign_key='universities.id')
    neighbourhood_id: int = Field(foreign_key='neighbourhoods.id')
    name: str = Field(max_length=50)
    sex: ProfileSex
    age: int
    profile_picture_url: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(SQLModel):
    uni_id: Optional[int] = None
    neighbourhood_id: Optional[int] = None
    name: Optional[str] = Field(default=None, max_length=50)
    sex: Optional[ProfileSex] = None
    age: Optional[int] = None
    profile_picture_url: Optional[str] = None


class ProfilePublic(ProfileBase, IDModel):
    pass


class ProfileModel(ProfileBase, IDModel, table=True):
    __tablename__ = 'profiles'

    user: 'UserModel' = Relationship(back_populates='profile')
    university: Optional['UniversityModel'] = Relationship(back_populates='profiles')
    neighbourhood: Optional['NeighbourhoodModel'] = Relationship(back_populates='profiles')

    tags: list[TagModel] = Relationship(back_populates='profiles', link_model=ProfileTagLink)
    sent_reactions: list['ReactionModel'] = Relationship(back_populates='profile')
    deals: list['DealModel'] = Relationship(back_populates='owner_profile')
    chats: list['ChatModel'] = Relationship(back_populates='profile')