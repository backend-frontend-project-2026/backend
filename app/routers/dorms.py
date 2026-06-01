from typing import Annotated

from fastapi import APIRouter, Depends, Security

from app.dependencies.auth import get_current_user
from app.dependencies.services import DormServiceDep
from app.exceptions.base import NotFoundError
from app.exceptions.responses import common_error_responses, create_error_responses
from app.models.dorms import DormCreate, DormUpdate
from app.models.users import UserModel
from app.schemas.dorms import (
    DormFilters,
    DormListResponse,
    DormResponse,
)

router = APIRouter(prefix='/universities/{university_id}/dorms', tags=['Dorms'])


@router.get(
    '',
    response_model=DormListResponse,
    responses=common_error_responses,
)
async def list_dorms(
    dorm_service: DormServiceDep,
    filters: Annotated[DormFilters, Depends()],
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:read'],
    ),
):
    return await dorm_service.get_list(filters)


@router.post(
    '',
    response_model=DormResponse,
    responses=create_error_responses,
)
async def create_dorm(
    university_id: int,
    dorm_create: DormCreate,
    dorm_service: DormServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:create'],
    ),
):
    return await dorm_service.create(dorm_create, uni_id=university_id)


@router.get(
    '/{dorm_id}',
    response_model=DormResponse,
    responses=common_error_responses,
)
async def get_dorm(
    university_id: int,
    dorm_id: int,
    dorm_service: DormServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:read'],
    ),
):
    dorm = await dorm_service.get_by_id(dorm_id)
    if dorm is None or dorm.uni_id != university_id:
        raise NotFoundError('Dorm or university not found')
    return dorm


@router.put(
    '/{dorm_id}',
    response_model=DormResponse,
    responses=common_error_responses,
)
async def update_dorm(
    university_id: int,
    dorm_id: int,
    dorm_update: DormUpdate,
    dorm_service: DormServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:update'],
    ),
):
    existing_dorm = await dorm_service.get_by_id(dorm_id)
    if existing_dorm is None or existing_dorm.uni_id != university_id:
        raise NotFoundError('Dorm or university not found')

    dorm = await dorm_service.update(
        dorm_id,
        dorm_update,
    )
    if dorm is None:
        raise NotFoundError('Dorm or university not found')
    return dorm


@router.delete(
    '/{dorm_id}',
    response_model=DormResponse,
    responses=common_error_responses,
)
async def delete_dorm(
    university_id: int,
    dorm_id: int,
    dorm_service: DormServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:delete'],
    ),
):
    dorm = await dorm_service.get_by_id(dorm_id)
    if dorm is None or dorm.uni_id != university_id:
        raise NotFoundError('Dorm or university not found')

    deleted_dorm = await dorm_service.delete(dorm_id)
    if deleted_dorm is None:
        raise NotFoundError('Dorm or university not found')
    return deleted_dorm