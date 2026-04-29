from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

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
