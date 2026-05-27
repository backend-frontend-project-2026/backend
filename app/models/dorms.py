from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel as SchemaModel
from pydantic import Field as SchemaField
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel
from app.schemas.base import IDSchema

if TYPE_CHECKING:
    from app.models.deals import DealModel
    from app.models.universities import UniversityModel


class DormBase(SQLModel):
    uni_id: int = Field(foreign_key='universities.id')
    name: str = Field(max_length=255)
    city: str
    address: str = Field(max_length=255)


class DormCreate(DormBase):
    pass


class DormUpdate(SchemaModel):
    uni_id: Optional[int] = None
    name: Optional[str] = SchemaField(default=None, max_length=255)
    city: Optional[str] = None
    address: Optional[str] = SchemaField(default=None, max_length=255)


class DormPublic(DormBase, IDSchema):
    pass


class DormModel(DormBase, IDModel, TimestampedModel, table=True):
    __tablename__ = 'dorms'

    university: Optional['UniversityModel'] = Relationship(back_populates='dorms')
    deals: list['DealModel'] = Relationship(back_populates='dorm')