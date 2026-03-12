from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.users import UserModel
    from app.models.neighbourhoods import NeighbourhoodModel
    from app.models.universities import UniversityModel


class ProfileSex(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


class ProfileModel(BaseModel, table=True):
    user_id: int = Field(foreign_key='user.id', unique=True)
    name: str = Field(max_length=50)
    sex: ProfileSex
    age: int
    profile_picture_url: str
    #tags_id: List[int] = Field(sa_column=Column(ARRAY(Integer), nullable=False))
    uni_id: int = Field(foreign_key='UniversityModel.id')
    neighbourhood_id: int = Field(foreign_key='NeighbourhoodModel.id')

    user: Optional['UserModel'] = Relationship(back_populates='profile')
    university: Optional['UniversityModel'] = Relationship()
    neighbourhood: Optional['NeighbourhoodModel'] = Relationship()
