from datetime import datetime, timezone
from enum import Enum
from typing import Optional

import sqlalchemy as sa
from pydantic import EmailStr
from sqlmodel import Field

from app.models.base import IDModel, TimestampedModel


class EmailNotificationAction(str, Enum):
    CONFIRM_ACCOUNT = 'CONFIRM_ACCOUNT'
    RESET_PASSWORD = 'RESET_PASSWORD'


class EmailNotificationModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'email_notifications'

    user_id: int = Field(foreign_key='users.id', index=True)
    recipient_email: EmailStr = Field(max_length=255, index=True)
    action: EmailNotificationAction = Field(index=True)
    code: str = Field(max_length=64, index=True)
    is_used: bool = Field(default=False)
    expires_at: datetime = Field(
        sa_column=sa.Column(sa.TIMESTAMP(timezone=True), nullable=False),
    )
    used_at: Optional[datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.TIMESTAMP(timezone=True), nullable=True),
    )

    @property
    def is_expired(self) -> bool:
        expires_at = self.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) >= expires_at

    @property
    def is_valid(self) -> bool:
        return not self.is_used and not self.is_expired