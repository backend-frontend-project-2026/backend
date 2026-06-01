from typing import Annotated

from fastapi import APIRouter, Depends, Security

from app.dependencies.auth import get_current_user
from app.dependencies.services import ProfileServiceDep
from app.exceptions.base import ConflictError, NotFoundError
from app.exceptions.responses import common_error_responses, create_error_responses
from app.models.profiles import ProfileCreate, ProfileUpdate
from app.models.users import UserModel
from app.schemas.profiles import (
    ProfileFilters,
    ProfileListResponse,
    ProfileResponse,
)

router = APIRouter(tags=['Profiles'])
user_profile_router = APIRouter(prefix='/users/{user_id}/profile', tags=['Profiles'])


@router.get(
    '/profiles',
    response_model=ProfileListResponse,
    responses=common_error_responses,
)
async def list_profiles(
    profile_service: ProfileServiceDep,
    filters: Annotated[ProfileFilters, Depends()],
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['profiles:read'],
    ),
):
    return await profile_service.get_list(filters)


@user_profile_router.get(
    '',
    response_model=ProfileResponse,
    responses=common_error_responses,
)
async def get_profile(
    user_id: int,
    profile_service: ProfileServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['profiles:read'],
    ),
):
    profile = await profile_service.get_profile_by_user_id(user_id)
    if profile is None:
        raise NotFoundError('User or profile not found')
    return profile


@user_profile_router.post(
    '',
    response_model=ProfileResponse,
    responses=create_error_responses,
)
async def create_profile(
    user_id: int,
    profile_create: ProfileCreate,
    profile_service: ProfileServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['profiles:create'],
    ),
):
    existing_profile = await profile_service.get_profile_by_user_id(user_id)
    if existing_profile is not None:
        raise ConflictError('Profile already exists')

    return await profile_service.create(profile_create, user_id=user_id)


@user_profile_router.put(
    '',
    response_model=ProfileResponse,
    responses=common_error_responses,
)
async def update_profile(
    user_id: int,
    profile_update: ProfileUpdate,
    profile_service: ProfileServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['profiles:update'],
    ),
):
    profile = await profile_service.update_profile(user_id, profile_update)
    if profile is None:
        raise NotFoundError('User or profile not found')
    return profile


@user_profile_router.delete(
    '',
    response_model=ProfileResponse,
    responses=common_error_responses,
)
async def delete_profile(
    user_id: int,
    profile_service: ProfileServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['profiles:delete'],
    ),
):
    profile = await profile_service.delete_profile(user_id)
    if profile is None:
        raise NotFoundError('User or profile not found')
    return profile


router.include_router(user_profile_router)