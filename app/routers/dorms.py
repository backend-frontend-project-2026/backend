from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies.services import DormServiceDep
from app.schemas.dorms import (
    DormCreate,
    DormFilters,
    DormListResponse,
    DormResponse,
    DormUpdate,
)

router = APIRouter(prefix='/universities/{university_id}/dorms', tags=['Dorms'])


@router.get('')
async def list_dorms(
    dorm_service: DormServiceDep,
    filters: Annotated[DormFilters, Depends()],
) -> DormListResponse:
    return await dorm_service.get_list(filters)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_dorm(
    university_id: int,
    dorm_create: DormCreate,
    dorm_service: DormServiceDep,
) -> DormResponse:
    return await dorm_service.create(dorm_create, uni_id=university_id)


@router.get('/{dorm_id}')
async def get_dorm(
    university_id: int,
    dorm_id: int,
    dorm_service: DormServiceDep,
) -> DormResponse:
    dorm = await dorm_service.get_by_id(dorm_id)
    if dorm is None or dorm.uni_id != university_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Dorm or university not found'
        )
    return dorm


@router.put('/{dorm_id}')
async def update_dorm(
    university_id: int,
    dorm_id: int,
    dorm_update: DormUpdate,
    dorm_service: DormServiceDep,
) -> DormResponse:
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


@router.delete('/{dorm_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_dorm(
    university_id: int,
    dorm_id: int,
    dorm_service: DormServiceDep,
) -> Response:
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
    return Response(status_code=status.HTTP_204_NO_CONTENT)
