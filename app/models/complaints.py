from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel

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


class ComplaintBase(TimestampedModel):
    complainant_id: int = Field(foreign_key='users.id')
    reported_user_id: int = Field(foreign_key='users.id')
    reason: str = Field(max_length=1000)
    status: ComplaintStatus = Field(default=ComplaintStatus.NEW)
    screenshots: Optional[str] = None


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintUpdate(SQLModel):
    status: Optional[ComplaintStatus] = None
    screenshots: Optional[str] = None


class ComplaintPublic(ComplaintBase, IDModel):
    pass


class ComplaintModel(ComplaintBase, IDModel, table=True):
    __tablename__ = 'complaints'

    complainant: Optional['UserModel'] = Relationship(
        back_populates='sent_complaints',
        sa_relationship_kwargs={
            'foreign_keys': '[ComplaintModel.complainant_id]',
        },
    )
    reported_user: Optional['UserModel'] = Relationship(
        back_populates='received_complaints',
        sa_relationship_kwargs={'foreign_keys': '[ComplaintModel.reported_user_id]'},
    )
