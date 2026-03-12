from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.users import ProfileModel


class DislikeModel(BaseModel, table=True):
    profile_id: int = Field(foreign_key="ProfileModel.id", primary_key=True)
    disliked_profile_id: int = Field(foreign_key="ProfileModel.id", primary_key=True)

    owner: "ProfileModel" = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "lambda: [DislikeModel.profile_id]"
        }
    )

    target: "ProfileModel" = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "lambda: [DislikeModel.disliked_profile_id]"
        }
    )
