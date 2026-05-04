from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel as SchemaModel
from pydantic import Field as SchemaField
from sqlmodel import Field, Relationship

from app.models.base import IDModel, TimestampedModel
from app.models.tags import ProfileTagLink, TagModel
from app.schemas.base import CreatedAtSchema, IDSchema

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


class ProfileBase(SchemaModel):
    uni_id: int
    faculty_id: int
    name: str = SchemaField(max_length=50)
    sex: ProfileSex
    age: int = SchemaField(ge=16)
    profile_description: Optional[str] = None
    course: Optional[int] = SchemaField(default=None, ge=1)
    city: str
    neighbourhood_id: Optional[int] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(SchemaModel):
    uni_id: Optional[int] = None
    faculty_id: Optional[int] = None
    name: Optional[str] = SchemaField(default=None, max_length=50)
    sex: Optional[ProfileSex] = None
    age: Optional[int] = SchemaField(default=None, ge=16)
    profile_description: Optional[str] = None
    course: Optional[int] = SchemaField(default=None, ge=1)
    city: Optional[str] = None
    neighbourhood_id: Optional[int] = None


class ProfilePublic(ProfileBase, IDSchema, CreatedAtSchema):
    user_id: int


class ProfileModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'profiles'

    uni_id: int = Field(foreign_key='universities.id')
    faculty_id: int = Field(foreign_key='faculties.id')
    name: str = Field(max_length=50)
    sex: ProfileSex
    age: int = Field(ge=16)
    profile_description: Optional[str] = None
    course: Optional[int] = Field(default=None, ge=1)
    city: str
    neighbourhood_id: Optional[int] = Field(
        default=None, foreign_key='neighbourhoods.id'
    )
    user_id: int = Field(foreign_key='users.id', unique=True)

    user: Optional['UserModel'] = Relationship(back_populates='profile')
    university: Optional['UniversityModel'] = Relationship(back_populates='profiles')
    neighbourhood: Optional['NeighbourhoodModel'] = Relationship(
        back_populates='profiles'
    )

    tags: list['TagModel'] = Relationship(
        back_populates='profiles',
        link_model=ProfileTagLink,
    )
    sent_reactions: list['ReactionModel'] = Relationship(back_populates='profile')
    deals: list['DealModel'] = Relationship(back_populates='owner_profile')
    chats: list['ChatModel'] = Relationship(back_populates='profile')
