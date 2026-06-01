from typing import Annotated

from fastapi import APIRouter, Depends, Security

from app.dependencies.auth import get_current_user
from app.dependencies.services import UserServiceDep
from app.exceptions.base import NotFoundError
from app.exceptions.responses import common_error_responses
from app.models.users import UserModel, UserPublic, UserUpdate
from app.schemas.users import UserFilters, UserListResponse

router = APIRouter(prefix='/users', tags=['Users'])


@router.get(
    '',
    response_model=UserListResponse,
    responses=common_error_responses,
)
async def list_users(
    user_service: UserServiceDep,
    filters: Annotated[UserFilters, Depends()],
    _current_user: UserModel = Security(get_current_user, scopes=['users:read']),
):
    return await user_service.get_list(filters)


@router.get(
    '/{user_id}',
    response_model=UserPublic,
    responses=common_error_responses,
)
async def get_user(
    user_id: int,
    user_service: UserServiceDep,
    _current_user: UserModel = Security(get_current_user, scopes=['users:read']),
):
    user = await user_service.get_by_id(user_id)
    if user is None:
        raise NotFoundError('User not found')
    return user


@router.put(
    '/{user_id}',
    response_model=UserPublic,
    responses=common_error_responses,
)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_service: UserServiceDep,
    _current_user: UserModel = Security(get_current_user, scopes=['users:update']),
):
    user = await user_service.update_user(user_update, user_id)
    if user is None:
        raise NotFoundError('User not found')
    return user


@router.delete(
    '/{user_id}',
    response_model=UserPublic,
    responses=common_error_responses,
)
async def delete_user(
    user_id: int,
    user_service: UserServiceDep,
    _current_user: UserModel = Security(get_current_user, scopes=['users:delete']),
):
    deleted_user = await user_service.delete(user_id)
    if deleted_user is None:
        raise NotFoundError('User not found')
    return deleted_user