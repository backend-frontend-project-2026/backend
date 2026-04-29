from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies.services import UniversityServiceDep
from app.schemas.universities import (
    UniversityCreate,
    UniversityFilters,
    UniversityListResponse,
    UniversityResponse,
    UniversityUpdate,
)

router = APIRouter(prefix='/universities', tags=['Universities'])


@router.get('', response_model=UniversityListResponse)
async def list_universities(
    university_service: UniversityServiceDep,
    filters: Annotated[UniversityFilters, Depends()],
) -> UniversityListResponse:
    return await university_service.get_list(filters)


@router.post('', response_model=UniversityResponse, status_code=status.HTTP_201_CREATED)
async def create_university(
    university_create: UniversityCreate,
    university_service: UniversityServiceDep,
) -> UniversityResponse:
    return await university_service.create(university_create)


@router.get('/{university_id}', response_model=UniversityResponse)
async def get_university(
    university_id: int,
    university_service: UniversityServiceDep,
) -> UniversityResponse:
    university = await university_service.get_by_id(university_id)
    if university is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='University not found'
        )
    return university


@router.put('/{university_id}', response_model=UniversityResponse)
async def update_university(
    university_id: int,
    university_update: UniversityUpdate,
    university_service: UniversityServiceDep,
) -> UniversityResponse:
    university = await university_service.update(university_id, university_update)
    if university is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='University not found'
        )
    return university


@router.delete('/{university_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_university(
    university_id: int,
    university_service: UniversityServiceDep,
) -> Response:
    university = await university_service.delete(university_id)
    if university is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='University not found'
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
