from enum import Enum
from typing import TYPE_CHECKING, Optional

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


class UserModel(BaseModel, table=True):
    __tablename__ = 'users'

    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(unique=True, index=True)
    password_hash: str
    role: UserRole = Field(default=UserRole.STUDENT)
    status: UserStatus = Field(default=UserStatus.CREATED)

    sent_complaints: list['ComplaintModel'] = Relationship(
        back_populates='complainant',
        sa_relationship_kwargs={
            'lazy': 'selectin',
            'foreign_keys': '[ComplaintModel.complainant_id]',
        },
    )

    received_complaints: list['ComplaintModel'] = Relationship(
        back_populates='reported_user',
        sa_relationship_kwargs={
            'lazy': 'selectin',
            'foreign_keys': '[ComplaintModel.reported_user_id]',
        },
    )

    profile: Optional['ProfileModel'] = Relationship(
        back_populates='user',
        sa_relationship_kwargs={'uselist': False, 'lazy': 'joined'},
    )
