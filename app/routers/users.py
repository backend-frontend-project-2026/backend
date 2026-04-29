from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies.services import UserServiceDep
from app.schemas.users import UserFilters, UserListResponse, UserResponse, UserUpdate

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('')
async def list_users(
    user_service: UserServiceDep,
    filters: Annotated[UserFilters, Depends()],
) -> UserListResponse:
    return await user_service.get_list(filters)


@router.get('/{user_id}')
async def get_user(
    user_id: int,
    user_service: UserServiceDep,
) -> UserResponse:
    user = await user_service.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    return user


@router.put('/{user_id}')
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
    deleted_user = await user_service.delete(user_id)
    if deleted_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
