from typing import Annotated

from fastapi import APIRouter, Depends, Security, status

from app.dependencies.auth import get_current_user
from app.dependencies.session import SessionDep
from app.exceptions.base import NotFoundError
from app.exceptions.responses import common_error_responses, create_error_responses
from app.models.users import UserModel, UserPublic, UserRolesUpdate
from app.schemas.roles import (
    PermissionFilters,
    PermissionListResponse,
    RoleCreate,
    RoleFilters,
    RoleListResponse,
    RoleResponse,
    RoleUpdate,
)
from app.services.roles import RoleService

router = APIRouter(tags=['Roles & Permissions'])


def get_role_service(session: SessionDep) -> RoleService:
    return RoleService(session)


RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]


@router.get(
    '/roles',
    response_model=RoleListResponse,
    responses=common_error_responses,
)
async def list_roles(
    role_service: RoleServiceDep,
    filters: Annotated[RoleFilters, Depends()],
    _current_user: UserModel = Security(get_current_user, scopes=['roles:read']),
):
    return await role_service.get_roles(filters)


@router.get(
    '/roles/{role_id}',
    response_model=RoleResponse,
    responses=common_error_responses,
)
async def get_role(
    role_id: int,
    role_service: RoleServiceDep,
    _current_user: UserModel = Security(get_current_user, scopes=['roles:read']),
):
    role = await role_service.get_role(role_id)
    if role is None:
        raise NotFoundError('Role not found')
    return role


@router.post(
    '/roles',
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    responses=create_error_responses,
)
async def create_role(
    payload: RoleCreate,
    role_service: RoleServiceDep,
    _current_user: UserModel = Security(get_current_user, scopes=['roles:create']),
):
    return await role_service.create_role(payload)


@router.put(
    '/roles/{role_id}',
    response_model=RoleResponse,
    responses=common_error_responses,
)
async def update_role(
    role_id: int,
    payload: RoleUpdate,
    role_service: RoleServiceDep,
    _current_user: UserModel = Security(get_current_user, scopes=['roles:update']),
):
    role = await role_service.update_role(role_id, payload)
    if role is None:
        raise NotFoundError('Role not found')
    return role


@router.delete(
    '/roles/{role_id}',
    response_model=RoleResponse,
    responses=common_error_responses,
)
async def delete_role(
    role_id: int,
    role_service: RoleServiceDep,
    _current_user: UserModel = Security(get_current_user, scopes=['roles:delete']),
):
    role = await role_service.delete_role(role_id)
    if role is None:
        raise NotFoundError('Role not found')
    return role


@router.get(
    '/permissions',
    response_model=PermissionListResponse,
    responses=common_error_responses,
)
async def list_permissions(
    role_service: RoleServiceDep,
    filters: Annotated[PermissionFilters, Depends()],
    _current_user: UserModel = Security(get_current_user, scopes=['roles:read']),
):
    return await role_service.get_permissions(filters)


@router.put(
    '/users/{user_id}/roles',
    response_model=UserPublic,
    responses=common_error_responses,
)
async def assign_user_roles(
    user_id: int,
    payload: UserRolesUpdate,
    role_service: RoleServiceDep,
    _current_user: UserModel = Security(get_current_user, scopes=['users:update']),
):
    user = await role_service.assign_roles_to_user(user_id, payload.role_ids)
    if user is None:
        raise NotFoundError('User not found')

    return UserPublic(
        id=user.id,
        created_at=user.created_at,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        status=user.status,
        roles=[role.name for role in user.roles],
    )
