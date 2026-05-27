from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel as SchemaModel
from pydantic import EmailStr
from pydantic import Field as SchemaField
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel
from app.schemas.base import CreatedAtSchema, IDSchema

if TYPE_CHECKING:
    from app.models.complaints import ComplaintModel
    from app.models.profiles import ProfileModel


class UserRole(str, Enum):
    STUDENT = 'STUDENT'
    ADMIN = 'ADMIN'
    MODERATOR = 'MODERATOR'


class UserStatus(str, Enum):
    CREATED = 'CREATED'
    CONFIRMED = 'CONFIRMED'
    BANNED = 'BANNED'


class UserBase(SQLModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(index=True)
    role: UserRole = Field(default=UserRole.STUDENT)
    status: UserStatus = Field(default=UserStatus.CREATED)


class UserCreate(UserBase):
    password: str = SchemaField(min_length=8, max_length=128)


class UserUpdate(SchemaModel):
    first_name: Optional[str] = SchemaField(default=None, max_length=50)
    last_name: Optional[str] = SchemaField(default=None, max_length=50)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    password: Optional[str] = SchemaField(default=None, min_length=8, max_length=128)


class UserPublic(UserBase, IDSchema, CreatedAtSchema):
    pass


class UserModel(UserBase, IDModel, TimestampedModel, table=True):
    __tablename__ = 'users'

    password_hash: str

    sent_complaints: list['ComplaintModel'] = Relationship(
        back_populates='complainant',
        sa_relationship_kwargs={
            'foreign_keys': '[ComplaintModel.complainant_id]',
        },
    )
    received_complaints: list['ComplaintModel'] = Relationship(
        back_populates='reported_user',
        sa_relationship_kwargs={
            'foreign_keys': '[ComplaintModel.reported_user_id]',
        },
    )
    profile: Optional['ProfileModel'] = Relationship(back_populates='user')