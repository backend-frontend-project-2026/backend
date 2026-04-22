from fastapi import APIRouter, HTTPException, Query, Response, status

from app.dependencies.services import ProfileServiceDep, UserServiceDep
from app.models.users import UserRole
from app.schemas.profiles import ProfileCreate, ProfileResponse, ProfileUpdate
from app.schemas.users import UserFilters, UserListResponse, UserResponse, UserUpdate

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('', response_model=UserListResponse)
async def list_users(
    user_service: UserServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    email: str | None = None,
    role: UserRole | None = None,
) -> UserListResponse:
    return await user_service.get_users(
        UserFilters(page=page, page_size=page_size, email=email, role=role)
    )


@router.get('/{user_id}', response_model=UserResponse)
async def get_user(
    user_id: int,
    user_service: UserServiceDep,
) -> UserResponse:
    user = await user_service.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    return user


@router.put('/{user_id}', response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_service: UserServiceDep,
) -> UserResponse:
    user = await user_service.update_user(user_update, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    return user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user_service: UserServiceDep,
) -> Response:
    deleted_user = await user_service.delete_user(user_id)
    if deleted_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/{user_id}/profile', response_model=ProfileResponse, tags=['Profiles'])
async def get_profile(
    user_id: int,
    profile_service: ProfileServiceDep,
) -> ProfileResponse:
    profile = await profile_service.get_profile_by_user_id(user_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User or profile not found'
        )
    return profile


@router.post(
    '/{user_id}/profile',
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Profiles'],
)
async def create_profile(
    user_id: int,
    profile_create: ProfileCreate,
    profile_service: ProfileServiceDep,
) -> ProfileResponse:
    existing_profile = await profile_service.get_profile_by_user_id(user_id)
    if existing_profile is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Profile already exists'
        )
    return await profile_service.create_profile(user_id, profile_create)


@router.put('/{user_id}/profile', response_model=ProfileResponse, tags=['Profiles'])
async def update_profile(
    user_id: int,
    profile_update: ProfileUpdate,
    profile_service: ProfileServiceDep,
) -> ProfileResponse:
    profile = await profile_service.update_profile(user_id, profile_update)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User or profile not found'
        )
    return profile


@router.delete(
    '/{user_id}/profile', status_code=status.HTTP_204_NO_CONTENT, tags=['Profiles']
)
async def delete_profile(
    user_id: int,
    profile_service: ProfileServiceDep,
) -> Response:
    profile = await profile_service.delete_profile(user_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User or profile not found'
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
