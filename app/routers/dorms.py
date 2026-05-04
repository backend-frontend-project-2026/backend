from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies.services import DormServiceDep
from app.models.dorms import DormCreate, DormUpdate
from app.schemas.dorms import (
    DormFilters,
    DormListResponse,
    DormResponse,
)

router = APIRouter(prefix='/universities/{university_id}/dorms', tags=['Dorms'])


@router.get('', response_model=DormListResponse)
async def list_dorms(
    dorm_service: DormServiceDep,
    filters: Annotated[DormFilters, Depends()],
):
    return await dorm_service.get_list(filters)


@router.post('', response_model=DormResponse)
async def create_dorm(
    university_id: int,
    dorm_create: DormCreate,
    dorm_service: DormServiceDep,
):
    return await dorm_service.create(dorm_create, uni_id=university_id)


@router.get('/{dorm_id}', response_model=DormResponse)
async def get_dorm(
    university_id: int,
    dorm_id: int,
    dorm_service: DormServiceDep,
):
    dorm = await dorm_service.get_by_id(dorm_id)
    if dorm is None or dorm.uni_id != university_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Dorm or university not found'
        )
    return dorm


@router.put('/{dorm_id}', response_model=DormResponse)
async def update_dorm(
    university_id: int,
    dorm_id: int,
    dorm_update: DormUpdate,
    dorm_service: DormServiceDep,
):
    existing_dorm = await dorm_service.get_by_id(dorm_id)
    if existing_dorm is None or existing_dorm.uni_id != university_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Dorm or university not found'
        )
    dorm = await dorm_service.update(
        dorm_id,
        dorm_update,
    )
    if dorm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Dorm or university not found'
        )
    return dorm


@router.delete('/{dorm_id}', response_model=DormResponse)
async def delete_dorm(
    university_id: int,
    dorm_id: int,
    dorm_service: DormServiceDep,
):
    dorm = await dorm_service.get_by_id(dorm_id)
    if dorm is None or dorm.uni_id != university_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Dorm or university not found'
        )
    deleted_dorm = await dorm_service.delete(dorm_id)
    if deleted_dorm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Dorm or university not found'
        )
    return deleted_dorm
