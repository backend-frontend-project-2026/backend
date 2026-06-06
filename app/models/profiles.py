from datetime import date
from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel as SchemaModel
from pydantic import Field as SchemaField
from sqlalchemy import JSON, Column, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import Field, Relationship

from app.models.base import IDModel, TimestampedModel
from app.models.tags import ProfileTagLink, TagModel
from app.schemas.base import CreatedAtSchema, IDSchema

if TYPE_CHECKING:
    from app.models.chats import ChatModel
    from app.models.deals import DealModel
    from app.models.neighbourhoods import NeighbourhoodModel
    from app.models.reactions import ReactionModel
    from app.models.universities import UniversityModel
    from app.models.users import UserModel


class ProfileSex(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


class ProfileBase(SchemaModel):
    user_id: int
    uni_id: int
    faculty_id: Optional[int] = None
    neighbourhood_id: Optional[int] = None

    name: str = SchemaField(max_length=50)
    sex: ProfileSex
    age: int
    course: Optional[int] = None
    city: Optional[str] = SchemaField(default=None, max_length=100)
    profile_description: Optional[str] = None

    avatar_url: Optional[str] = None
    photo_urls: list[str] = SchemaField(default_factory=list)

    sleep_schedule: Optional[str] = SchemaField(default=None, max_length=100)
    cleanliness: Optional[str] = SchemaField(default=None, max_length=100)
    noise_level: Optional[str] = SchemaField(default=None, max_length=100)
    guest_frequency: Optional[str] = SchemaField(default=None, max_length=100)
    smoking_preference: Optional[str] = SchemaField(default=None, max_length=100)
    alcohol_preference: Optional[str] = SchemaField(default=None, max_length=100)
    room_order_preference: Optional[str] = SchemaField(default=None, max_length=150)
    pet_preference: Optional[str] = SchemaField(default=None, max_length=100)

    has_quiet_hours: bool = False
    quiet_from: Optional[str] = SchemaField(default=None, max_length=10)
    quiet_to: Optional[str] = SchemaField(default=None, max_length=10)
    is_smoking_allowed: bool = False
    has_pets: bool = False

    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    move_in_date: Optional[date] = None
    stay_duration: Optional[str] = SchemaField(default=None, max_length=100)
    housing_type: Optional[str] = SchemaField(default=None, max_length=100)
    living_notes: Optional[str] = None
    ideal_roommate_description: Optional[str] = None
    rental_criteria: Optional[str] = None

    interests: list[str] = SchemaField(default_factory=list)

    compatibility_note: Optional[str] = None


class ProfileCreate(ProfileBase):
    user_id: Optional[int] = None


class ProfileUpdate(SchemaModel):
    user_id: Optional[int] = None
    uni_id: Optional[int] = None
    faculty_id: Optional[int] = None
    neighbourhood_id: Optional[int] = None

    name: Optional[str] = SchemaField(default=None, max_length=50)
    sex: Optional[ProfileSex] = None
    age: Optional[int] = None
    course: Optional[int] = None
    city: Optional[str] = SchemaField(default=None, max_length=100)
    profile_description: Optional[str] = None

    avatar_url: Optional[str] = None
    photo_urls: Optional[list[str]] = None

    sleep_schedule: Optional[str] = SchemaField(default=None, max_length=100)
    cleanliness: Optional[str] = SchemaField(default=None, max_length=100)
    noise_level: Optional[str] = SchemaField(default=None, max_length=100)
    guest_frequency: Optional[str] = SchemaField(default=None, max_length=100)
    smoking_preference: Optional[str] = SchemaField(default=None, max_length=100)
    alcohol_preference: Optional[str] = SchemaField(default=None, max_length=100)
    room_order_preference: Optional[str] = SchemaField(default=None, max_length=150)
    pet_preference: Optional[str] = SchemaField(default=None, max_length=100)

    has_quiet_hours: Optional[bool] = None
    quiet_from: Optional[str] = SchemaField(default=None, max_length=10)
    quiet_to: Optional[str] = SchemaField(default=None, max_length=10)
    is_smoking_allowed: Optional[bool] = None
    has_pets: Optional[bool] = None

    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    move_in_date: Optional[date] = None
    stay_duration: Optional[str] = SchemaField(default=None, max_length=100)
    housing_type: Optional[str] = SchemaField(default=None, max_length=100)
    living_notes: Optional[str] = None
    ideal_roommate_description: Optional[str] = None
    rental_criteria: Optional[str] = None

    interests: Optional[list[str]] = None
    compatibility_note: Optional[str] = None


class ProfilePublic(ProfileBase, IDSchema, CreatedAtSchema):
    pass


class ProfileModel(IDModel, TimestampedModel, table=True):
    __tablename__ = 'profiles'

    user_id: int = Field(foreign_key='users.id', unique=True)
    uni_id: int = Field(foreign_key='universities.id')
    faculty_id: Optional[int] = Field(default=None, foreign_key='faculties.id')
    neighbourhood_id: Optional[int] = Field(
        default=None,
        foreign_key='neighbourhoods.id',
    )

    name: str = Field(max_length=50)
    sex: ProfileSex
    age: int
    course: Optional[int] = None
    city: Optional[str] = Field(default=None, max_length=100)
    profile_description: Optional[str] = None

    avatar_url: Optional[str] = None
    photo_urls: list[str] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(String()).with_variant(JSON(), 'sqlite'), nullable=False),
    )

    sleep_schedule: Optional[str] = Field(default=None, max_length=100)
    cleanliness: Optional[str] = Field(default=None, max_length=100)
    noise_level: Optional[str] = Field(default=None, max_length=100)
    guest_frequency: Optional[str] = Field(default=None, max_length=100)
    smoking_preference: Optional[str] = Field(default=None, max_length=100)
    alcohol_preference: Optional[str] = Field(default=None, max_length=100)
    room_order_preference: Optional[str] = Field(default=None, max_length=150)
    pet_preference: Optional[str] = Field(default=None, max_length=100)

    has_quiet_hours: bool = False
    quiet_from: Optional[str] = Field(default=None, max_length=10)
    quiet_to: Optional[str] = Field(default=None, max_length=10)
    is_smoking_allowed: bool = False
    has_pets: bool = False

    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    move_in_date: Optional[date] = None
    stay_duration: Optional[str] = Field(default=None, max_length=100)
    housing_type: Optional[str] = Field(default=None, max_length=100)
    living_notes: Optional[str] = None
    ideal_roommate_description: Optional[str] = None
    rental_criteria: Optional[str] = None

    interests: list[str] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(String()).with_variant(JSON(), 'sqlite'), nullable=False),
    )

    compatibility_note: Optional[str] = None

    user: Optional['UserModel'] = Relationship(back_populates='profile')
    university: Optional['UniversityModel'] = Relationship(back_populates='profiles')
    neighbourhood: Optional['NeighbourhoodModel'] = Relationship(back_populates='profiles')

    tags: list[TagModel] = Relationship(back_populates='profiles', link_model=ProfileTagLink)
    sent_reactions: list['ReactionModel'] = Relationship(back_populates='profile')
    deals: list['DealModel'] = Relationship(back_populates='owner_profile')
    chats: list['ChatModel'] = Relationship(back_populates='profile')