from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security, status

from app.dependencies.auth import get_current_user
from app.dependencies.session import SessionDep
from app.models.users import UserModel, UserRolesUpdate
from app.schemas.roles import (
    PermissionFilters,
    PermissionListResponse,
    RoleCreate,
    RoleFilters,
    RoleListResponse,
    RoleResponse,
    RoleUpdate,
)
from app.schemas.users import UserResponse
from app.services.roles import RoleService

router = APIRouter(tags=['Roles & Permissions'])


def get_role_service(session: SessionDep) -> RoleService:
    return RoleService(session)


RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]


@router.get('/roles', response_model=RoleListResponse)
async def list_roles(
    role_service: RoleServiceDep,
    filters: Annotated[RoleFilters, Depends()],
    _: UserModel = Security(get_current_user, scopes=['roles:read']),
):
    return await role_service.get_roles(filters)


@router.get('/roles/{role_id}', response_model=RoleResponse)
async def get_role(
    role_id: int,
    role_service: RoleServiceDep,
    _: UserModel = Security(get_current_user, scopes=['roles:read']),
):
    role = await role_service.get_role(role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Role not found'
        )
    return role


@router.post('/roles', response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    payload: RoleCreate,
    role_service: RoleServiceDep,
    _: UserModel = Security(get_current_user, scopes=['roles:create']),
):
    return await role_service.create_role(payload)


@router.put('/roles/{role_id}', response_model=RoleResponse)
async def update_role(
    role_id: int,
    payload: RoleUpdate,
    role_service: RoleServiceDep,
    _: UserModel = Security(get_current_user, scopes=['roles:update']),
):
    role = await role_service.update_role(role_id, payload)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Role not found'
        )
    return role


@router.delete('/roles/{role_id}', response_model=RoleResponse)
async def delete_role(
    role_id: int,
    role_service: RoleServiceDep,
    _: UserModel = Security(get_current_user, scopes=['roles:delete']),
):
    role = await role_service.delete_role(role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Role not found'
        )
    return role


@router.get('/permissions', response_model=PermissionListResponse)
async def list_permissions(
    role_service: RoleServiceDep,
    filters: Annotated[PermissionFilters, Depends()],
    _: UserModel = Security(get_current_user, scopes=['roles:read']),
):
    return await role_service.get_permissions(filters)


@router.put('/users/{user_id}/roles', response_model=UserResponse)
async def assign_user_roles(
    user_id: int,
    payload: UserRolesUpdate,
    role_service: RoleServiceDep,
    _: UserModel = Security(get_current_user, scopes=['users:update']),
):
    user = await role_service.assign_roles_to_user(user_id, payload.role_ids)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    return UserResponse.model_validate(user)
