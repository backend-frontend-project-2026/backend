from datetime import datetime, timedelta, timezone
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field

from app.models.base import IDModel, TimestampedModel


class EmailVerificationCodeModel(TimestampedModel, IDModel, table=True):
    __tablename__ = 'email_verification_codes'

    email: EmailStr = Field(index=True, max_length=255)
    code: str = Field(index=True, unique=True, max_length=6)
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(minutes=15)
    )
    used_at: Optional[datetime] = None


class PasswordResetTokenModel(TimestampedModel, IDModel, table=True):
    __tablename__ = 'password_reset_tokens'

    user_id: int = Field(foreign_key='users.id', index=True)
    token: str = Field(index=True, unique=True, max_length=255)
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=1)
    )
    used_at: Optional[datetime] = None