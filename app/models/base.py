from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import TIMESTAMP
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    pass


class TimestampedModel(BaseModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
        sa_column_kwargs={
            'onupdate': lambda: datetime.now(timezone.utc),
        },
    )


class IDModel(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
