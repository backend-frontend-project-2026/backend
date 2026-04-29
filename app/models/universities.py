from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.dorms import DormModel
    from app.models.faculties import FacultyModel
    from app.models.profiles import ProfileModel

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
