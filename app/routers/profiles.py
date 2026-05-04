from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies.services import ProfileServiceDep
from app.models.profiles import ProfileCreate, ProfileUpdate
from app.schemas.profiles import (
    ProfileFilters,
    ProfileListResponse,
    ProfileResponse,
)

router = APIRouter(tags=['Profiles'])
user_profile_router = APIRouter(prefix='/users/{user_id}/profile', tags=['Profiles'])

@router.get('/profiles', response_model=ProfileListResponse)
async def list_profiles(
    profile_service: ProfileServiceDep,
    filters: Annotated[ProfileFilters, Depends()],
):
    return await profile_service.get_list(filters)


@user_profile_router.get('', response_model=ProfileResponse)
async def get_profile(
    user_id: int,
    profile_service: ProfileServiceDep,
):
    profile = await profile_service.get_profile_by_user_id(user_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User or profile not found',
        )
    return profile


@user_profile_router.post(
    '',
    response_model=ProfileResponse,
)
async def create_profile(
    user_id: int,
    profile_create: ProfileCreate,
    profile_service: ProfileServiceDep,
):
    existing_profile = await profile_service.get_profile_by_user_id(user_id)
    if existing_profile is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Profile already exists',
        )
    return await profile_service.create(profile_create, user_id=user_id)


@user_profile_router.put('', response_model=ProfileResponse)
async def update_profile(
    user_id: int,
    profile_update: ProfileUpdate,
    profile_service: ProfileServiceDep,
):
    profile = await profile_service.update_profile(user_id, profile_update)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User or profile not found',
        )
    return profile


@user_profile_router.delete('', response_model=ProfileResponse)
async def delete_profile(
    user_id: int,
    profile_service: ProfileServiceDep,
):
    profile = await profile_service.delete_profile(user_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User or profile not found',
        )
    return profile

router.include_router(user_profile_router)
