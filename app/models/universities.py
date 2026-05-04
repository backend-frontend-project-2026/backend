from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel as SchemaModel
from pydantic import Field as SchemaField
from sqlmodel import Field, Relationship

from app.models.base import IDModel, TimestampedModel
from app.schemas.base import IDSchema

if TYPE_CHECKING:
    from app.models.dorms import DormModel
    from app.models.faculties import FacultyModel
    from app.models.profiles import ProfileModel


class UniversityBase(SchemaModel):
    name: str = SchemaField(max_length=255)
    city: str


class UniversityCreate(UniversityBase):
    pass


class UniversityUpdate(SchemaModel):
    name: Optional[str] = SchemaField(default=None, max_length=255)
    city: Optional[str] = None


class UniversityPublic(UniversityBase, IDSchema):
    pass


class UniversityModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'universities'

    name: str = Field(unique=True, max_length=255)
    city: str

    faculties: list['FacultyModel'] = Relationship(
        back_populates='university',
        sa_relationship_kwargs={'lazy': 'selectin', 'cascade': 'all, delete-orphan'},
    )
    dorms: list['DormModel'] = Relationship(
        back_populates='university',
        sa_relationship_kwargs={'lazy': 'selectin', 'cascade': 'all, delete-orphan'},
    )
    profiles: list['ProfileModel'] = Relationship(back_populates='university')
