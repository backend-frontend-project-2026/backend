from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel as SchemaModel
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel
from app.schemas.base import CreatedAtSchema, IDSchema

if TYPE_CHECKING:
    from app.models.users import UserModel


class ComplaintStatus(str, Enum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    RESOLVED = 'resolved'
    REJECTED = 'rejected'


class ComplaintReason(str, Enum):
    SPAM = 'spam'
    SCAM = 'scam'
    FAKE = 'fake'
    INAPPROPRIATE_CONTENT = 'inappropriate_content'
    OTHER = 'other'


class ComplaintBase(SQLModel):
    complainant_id: int = Field(foreign_key='users.id')
    reported_user_id: int = Field(foreign_key='users.id')
    reason: ComplaintReason
    screenshots: Optional[str] = Field(
        default=None,
        sa_column=Column('screenshot_url_for_report', String(), nullable=True),
    )
    status: ComplaintStatus = Field(default=ComplaintStatus.NEW)


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintUpdate(SchemaModel):
    status: Optional[ComplaintStatus] = None


class ComplaintPublic(ComplaintBase, IDSchema, CreatedAtSchema):
    pass


class ComplaintModel(ComplaintBase, IDModel, TimestampedModel, table=True):
    __tablename__ = 'complaints'

    complainant: Optional['UserModel'] = Relationship(
        back_populates='sent_complaints',
        sa_relationship_kwargs={
            'foreign_keys': '[ComplaintModel.complainant_id]',
        },
    )
    reported_user: Optional['UserModel'] = Relationship(
        back_populates='received_complaints',
        sa_relationship_kwargs={
            'foreign_keys': '[ComplaintModel.reported_user_id]',
        },
    )
