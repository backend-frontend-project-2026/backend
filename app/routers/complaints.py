from typing import Annotated

from fastapi import APIRouter, Depends, Security

from app.dependencies.auth import get_current_user
from app.dependencies.services import ComplaintServiceDep
from app.exceptions.base import NotFoundError
from app.exceptions.responses import common_error_responses, create_error_responses
from app.models.complaints import ComplaintCreate, ComplaintUpdate
from app.models.users import UserModel
from app.schemas.complaints import (
    ComplaintFilters,
    ComplaintListResponse,
    ComplaintResponse,
)

router = APIRouter(prefix='/complaints', tags=['Complaints'])


@router.get(
    '',
    response_model=ComplaintListResponse,
    responses=common_error_responses,
)
async def list_complaints(
    complaint_service: ComplaintServiceDep,
    filters: Annotated[ComplaintFilters, Depends()],
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['complaints:read'],
    ),
) -> ComplaintListResponse:
    return await complaint_service.get_list(filters)


@router.post(
    '',
    response_model=ComplaintResponse,
    responses=create_error_responses,
)
async def create_complaint(
    complaint_create: ComplaintCreate,
    complaint_service: ComplaintServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['complaints:create'],
    ),
):
    return await complaint_service.create(complaint_create)


@router.get(
    '/{complaint_id}',
    response_model=ComplaintResponse,
    responses=common_error_responses,
)
async def get_complaint(
    complaint_id: int,
    complaint_service: ComplaintServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['complaints:read'],
    ),
):
    complaint = await complaint_service.get_by_id(complaint_id)
    if complaint is None:
        raise NotFoundError('Complaint not found')
    return complaint


@router.put(
    '/{complaint_id}',
    response_model=ComplaintResponse,
    responses=common_error_responses,
)
async def update_complaint(
    complaint_id: int,
    complaint_update: ComplaintUpdate,
    complaint_service: ComplaintServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['complaints:update'],
    ),
):
    complaint = await complaint_service.update(complaint_id, complaint_update)
    if complaint is None:
        raise NotFoundError('Complaint not found')
    return complaint


@router.delete(
    '/{complaint_id}',
    response_model=ComplaintResponse,
    responses=common_error_responses,
)
async def delete_complaint(
    complaint_id: int,
    complaint_service: ComplaintServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['complaints:delete'],
    ),
):
    complaint = await complaint_service.delete(complaint_id)
    if complaint is None:
        raise NotFoundError('Complaint not found')
    return complaint