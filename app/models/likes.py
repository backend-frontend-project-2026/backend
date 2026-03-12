from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.profiles import ProfileModel


class LikeModel(BaseModel, table=True):
    profile_id: int = Field(foreign_key='ProfileModel.id')
    liked_profile_id: int = Field(foreign_key='ProfileModel.id')
