from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import TIMESTAMP
from sqlmodel import Field

from app.models.base import IDModel, TimestampedModel


class RefreshSessionModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'refresh_sessions'

    user_id: int = Field(foreign_key='users.id', index=True)

    access_token_jti: str = Field(index=True, unique=True, max_length=255)
    refresh_token_jti: str = Field(index=True, unique=True, max_length=255)

    expires_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
    )
    is_invalidated: bool = Field(default=False)

    invalidated_at: Optional[datetime] = Field(
        default=None,
        sa_type=TIMESTAMP(timezone=True),
    )

    @property
    def is_valid(self) -> bool:
        expires_at = self.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        return not self.is_invalidated and expires_at > datetime.now(timezone.utc)