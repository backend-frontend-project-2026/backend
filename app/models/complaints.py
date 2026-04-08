from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.users import UserModel


class ComplaintStatus(str, Enum):
    CREATED = 'created'
    RESOLVED = 'resolved'
    REJECTED = 'rejected'


class ComplaintReason(str, Enum):
    SPAM = 'spam'
    SCAM = 'scam'
    FAKE = 'fake'
    INAPPROPRIATE_CONTENT = 'inappropriate_content'

    OTHER = 'other'


class ComplaintModel(BaseModel, table=True):
    __tablename__ = 'complaints'

    complainant_id: int = Field(foreign_key='users.id')
    reported_user_id: int = Field(foreign_key='users.id')

    reason: ComplaintReason
    status: ComplaintStatus = Field(default=ComplaintStatus.CREATED)
    screenshot_url_for_report: Optional[str] = Field(default=None)

    complainant: 'UserModel' = Relationship(
        back_populates='sent_complaints',
        sa_relationship_kwargs={'foreign_keys': '[ComplaintModel.complainant_id]'},
    )
    reported_user: 'UserModel' = Relationship(
        back_populates='received_complaints',
        sa_relationship_kwargs={'foreign_keys': '[ComplaintModel.reported_user_id]'},
    )
