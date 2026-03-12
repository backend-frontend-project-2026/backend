from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel


class NeighbourhoodModel(BaseModel, table=True):
    district_name: str
