from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects.postgresql import TIMESTAMP

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.chats import ChatModel
    from app.models.profiles import ProfileModel


class MessageModel(BaseModel, table=True):
    chat_id: int = Field(foreign_key='ChatModel.id')
    profile_id: int = Field(foreign_key='ProfileModel.id')
    content: str
    # sent_at не добавил, потому что то же самое, что и created_at
    opened_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_type=TIMESTAMP(timezone=True), # type: ignore
    )
