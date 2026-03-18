from sqlmodel import SQLModel, Field, Relationship

from app.models.base import BaseModel

class TagModel(BaseModel, table=True):
    __tablename__ = 'tags'
    name: str = Field(unique=True)


class ProfileTagLink(SQLModel, table=True):
    __tablename__ = 'profile_tag_links'

    profile_id: int = Field(foreign_key='profiles.id', primary_key=True)
    tag_id: int = Field(foreign_key='tags.id', primary_key=True)
