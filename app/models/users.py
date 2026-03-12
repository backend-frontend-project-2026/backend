from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.complaints import ComplaintModel
    from app.models.profiles import ProfileModel

class UserStatus(str, Enum):
    CREATED = 'created'
    CONFIRMED = 'confirmed'
    BANNED = 'banned'


class UserRole(str, Enum):
    STUDENT = 'student'
    ADMIN = 'admin'
    MODERATOR = 'moderator'


class UserBase(SQLModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)


class UserPublic(BaseModel, UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserCreate(UserBase):
    password: str


class UserModel(UserPublic, table=True):
    email: str = Field(unique=True, index=True)
    password_hash: str
    role: UserRole = Field(default=UserRole.STUDENT)
    status: UserStatus = Field(default=UserStatus.CREATED)

    sent_complaints: list['ComplaintModel'] = Relationship(
        sa_relationship_kwargs={
            'lazy': 'selectin',
            'primaryjoin': 'UserModel.id == ComplaintModel.complainant_id'
        },
    )

    received_complaints: list['ComplaintModel'] = Relationship(
        sa_relationship_kwargs={
            'lazy': 'selectin',
            'primaryjoin': 'UserModel.id == ComplaintModel.reported_user_id'
        },
    )

    profile: Optional['ProfileModel'] = Relationship(
        back_populates='user',
        sa_relationship_kwargs={'uselist': False}
    )
