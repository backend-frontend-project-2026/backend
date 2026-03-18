from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import Field, SQLModel

from typing import Optional


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
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
