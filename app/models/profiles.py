from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

from app.models.tags import ProfileTagLink, TagModel

if TYPE_CHECKING:
    from app.models.users import UserModel
    from app.models.universities import UniversityModel
    from app.models.neighbourhoods import NeighbourhoodModel
    from app.models.tags import ProfileTagLink


class ProfileSex(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


class ProfileModel(BaseModel, table=True):
    __tablename__ = 'profiles'

    user_id: int = Field(foreign_key='users.id', unique=True)
    name: str = Field(max_length=50)
    sex: ProfileSex
    age: int
    profile_picture_url: Optional[str] = Field(default=None)

    tags: list[TagModel] = Relationship(
        back_populates='profiles', link_model=ProfileTagLink
    )

    uni_id: int = Field(foreign_key='universities.id')
    neighbourhood_id: int = Field(foreign_key='neighbourhoods.id')

    user: 'UserModel' = Relationship(back_populates='profile')

    sent_reactions: Optional[list['ReactionModel']] = Relationship(
        sa_relationship_kwargs={'foreign_keys': '[ReactionModel.profile_id]'},
    )
    received_reactions: Optional[list['ReactionModel']] = Relationship(
        sa_relationship_kwargs={'foreign_keys': '[ReactionModel.target_profile_id]'},
    )