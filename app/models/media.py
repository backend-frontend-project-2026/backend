from __future__ import annotations

from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.base import IDModel, TimestampedModel


class MediaKind(str, Enum):
    AVATAR = 'avatar'
    PROFILE_PHOTO = 'profile_photo'


class MediaUploadResponse(IDModel, SQLModel):
    url: str
    kind: Optional[MediaKind] = None
    filename: str


class MediaModel(TimestampedModel, IDModel, table=True):
    __tablename__ = 'media'

    kind: Optional[MediaKind] = None
    filename: str = Field(max_length=255)
    original_filename: str = Field(max_length=255)
    content_type: Optional[str] = Field(default=None, max_length=100)
    file_size: int
    url: str