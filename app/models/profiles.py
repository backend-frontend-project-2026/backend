from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.users import UserModel


class ProfileSex(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


class ProfileModel(BaseModel, table=True):
    __tablename__ = 'profiles'

    user_id: int = Field(foreign_key='users.id', unique=True)
    name: str = Field(max_length=50)
    sex: ProfileSex
    age: int
    profile_description: Optional[str] = Field(default=None)
    uni_id: int = Field(foreign_key='universities.id')
    faculty_id: int = Field(foreign_key='faculties.id')
    course: Optional[int] = Field(default=None)
    city: str
    neighbourhood_id: Optional[int] = Field(
        default=None, foreign_key='neighbourhoods.id'
    )

    user: 'UserModel' = Relationship(back_populates='profile')
