from fastapi import APIRouter, HTTPException, Query, Response, status

from app.dependencies.services import ProfileServiceDep
from app.models.profiles import ProfileSex
from app.schemas.profiles import (
    ProfileCreate,
    ProfileFilters,
    ProfileListResponse,
    ProfileResponse,
    ProfileUpdate,
)

router = APIRouter(prefix='/profiles', tags=['Profiles'])
user_profile_router = APIRouter(prefix='/users/{user_id}/profile', tags=['Profiles'])


@router.get('', response_model=ProfileListResponse)
async def list_profiles(
    profile_service: ProfileServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    sex: ProfileSex | None = None,
    age_min: int | None = None,
    age_max: int | None = None,
    uni_id: int | None = None,
    faculty_id: int | None = None,
    city: str | None = None,
    neighbourhood_id: int | None = None,
    tag_id: int | None = None,
    course: int | None = None,
) -> ProfileListResponse:
    filters = ProfileFilters(
        page=page,
        page_size=page_size,
        sex=sex,
        age_min=age_min,
        age_max=age_max,
        uni_id=uni_id,
        faculty_id=faculty_id,
        city=city,
        neighbourhood_id=neighbourhood_id,
        tag_id=tag_id,
        course=course,
    )
    return await profile_service.get_profiles(filters)


@user_profile_router.get('', response_model=ProfileResponse)
async def get_profile(
    user_id: int,
    profile_service: ProfileServiceDep,
) -> ProfileResponse:
    profile = await profile_service.get_profile_by_user_id(user_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User or profile not found',
        )
    return profile


@user_profile_router.post('', response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    user_id: int,
    profile_create: ProfileCreate,
    profile_service: ProfileServiceDep,
) -> ProfileResponse:
    existing_profile = await profile_service.get_profile_by_user_id(user_id)
    if existing_profile is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Profile already exists',
        )
    return await profile_service.create_profile(user_id, profile_create)


@user_profile_router.put('', response_model=ProfileResponse)
async def update_profile(
    user_id: int,
    profile_update: ProfileUpdate,
    profile_service: ProfileServiceDep,
) -> ProfileResponse:
    profile = await profile_service.update_profile(user_id, profile_update)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User or profile not found',
        )
    return profile


@user_profile_router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    user_id: int,
    profile_service: ProfileServiceDep,
) -> Response:
    profile = await profile_service.delete_profile(user_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User or profile not found',
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
