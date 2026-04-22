from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from app.models.base import IDModel, TimestampedModel


class UserBlockModel(TimestampedModel, IDModel, table=True):
    __tablename__ = 'user_blocks'
    __table_args__ = (
        UniqueConstraint('blocker_user_id', 'blocked_user_id', name='uq_user_block'),
    )

    blocker_user_id: int = Field(foreign_key='users.id')
    blocked_user_id: int = Field(foreign_key='users.id')