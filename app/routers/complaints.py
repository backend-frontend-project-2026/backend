from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies.services import ComplaintServiceDep
from app.schemas.complaints import (
    ComplaintCreate,
    ComplaintFilters,
    ComplaintListResponse,
    ComplaintResponse,
    ComplaintUpdate,
)

router = APIRouter(prefix='/complaints', tags=['Complaints'])


@router.get('', response_model=ComplaintListResponse)
async def list_complaints(
    complaint_service: ComplaintServiceDep,
    filters: Annotated[ComplaintFilters, Depends()],
) -> ComplaintListResponse:
    return await complaint_service.get_list(filters)


@router.post('', response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
async def create_complaint(
    complaint_create: ComplaintCreate,
    complaint_service: ComplaintServiceDep,
) -> ComplaintResponse:
    return await complaint_service.create(complaint_create)


@router.get('/{complaint_id}', response_model=ComplaintResponse)
async def get_complaint(
    complaint_id: int,
    complaint_service: ComplaintServiceDep,
) -> ComplaintResponse:
    complaint = await complaint_service.get_by_id(complaint_id)
    if complaint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Complaint not found'
        )
    return complaint


@router.put('/{complaint_id}', response_model=ComplaintResponse)
async def update_complaint(
    complaint_id: int,
    complaint_update: ComplaintUpdate,
    complaint_service: ComplaintServiceDep,
) -> ComplaintResponse:
    complaint = await complaint_service.update(complaint_id, complaint_update)
    if complaint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Complaint not found'
        )
    return complaint


@router.delete('/{complaint_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_complaint(
    complaint_id: int,
    complaint_service: ComplaintServiceDep,
) -> Response:
    complaint = await complaint_service.delete(complaint_id)
    if complaint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Complaint not found'
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
