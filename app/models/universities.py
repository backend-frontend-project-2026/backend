from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.dorms import DormModel
    from app.models.faculties import FacultyModel


class UniversityModel(BaseModel, table=True):
    __tablename__ = 'universities'
    
    name: str = Field(unique=True)

    dorms: list['DormModel'] = Relationship(
        back_populates='university',
        sa_relationship_kwargs={
            'lazy': 'selectin',
            'cascade': 'all, delete-orphan'
        },
    )

    faculties: list['FacultyModel'] = Relationship(
        back_populates='university',
        sa_relationship_kwargs={
            'lazy': 'selectin',
            'cascade': 'all, delete-orphan'
        },
    )
