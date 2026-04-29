from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.complaints import ComplaintModel
    from app.models.profiles import ProfileModel


class UserStatus(str, Enum):
    CREATED = 'created'
    CONFIRMED = 'confirmed'
    BANNED = 'banned'


class UserRole(str, Enum):
    USER = 'user'
    ADMIN = 'admin'

class UserModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'users'

    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(index=True)
    role: UserRole = Field(default=UserRole.USER)
    status: UserStatus = Field(default=UserStatus.CREATED)
    password_hash: str

    sent_complaints: list['ComplaintModel'] = Relationship(
        back_populates='complainant',
        sa_relationship_kwargs={'foreign_keys': '[ComplaintModel.complainant_id]'},
    )
    received_complaints: list['ComplaintModel'] = Relationship(
        back_populates='reported_user',
        sa_relationship_kwargs={'foreign_keys': '[ComplaintModel.reported_user_id]'},
    )
    profile: Optional['ProfileModel'] = Relationship(back_populates='user')
