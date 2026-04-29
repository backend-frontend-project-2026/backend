from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies.services import FacultyServiceDep
from app.schemas.faculties import (
    FacultyCreate,
    FacultyFilters,
    FacultyListResponse,
    FacultyResponse,
    FacultyUpdate,
)

router = APIRouter(prefix='/universities/{university_id}/faculties', tags=['Faculties'])


@router.get('')
async def list_faculties(
    faculty_service: FacultyServiceDep,
    filters: Annotated[FacultyFilters, Depends()],
) -> FacultyListResponse:
    return await faculty_service.get_list(filters)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_faculty(
    university_id: int,
    faculty_create: FacultyCreate,
    faculty_service: FacultyServiceDep,
) -> FacultyResponse:
    return await faculty_service.create(faculty_create, uni_id=university_id)


@router.get('/{faculty_id}')
async def get_faculty(
    university_id: int,
    faculty_id: int,
    faculty_service: FacultyServiceDep,
) -> FacultyResponse:
    faculty = await faculty_service.get_by_id(faculty_id)
    if faculty is None or faculty.uni_id != university_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Faculty or university not found',
        )
    return faculty


@router.put('/{faculty_id}')
async def update_faculty(
    university_id: int,
    faculty_id: int,
    faculty_update: FacultyUpdate,
    faculty_service: FacultyServiceDep,
) -> FacultyResponse:
    existing_faculty = await faculty_service.get_by_id(faculty_id)
    if existing_faculty is None or existing_faculty.uni_id != university_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Faculty or university not found',
        )
    faculty = await faculty_service.update(
        faculty_id,
        faculty_update,
    )
    if faculty is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Faculty or university not found',
        )
    return faculty


@router.delete('/{faculty_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_faculty(
    university_id: int,
    faculty_id: int,
    faculty_service: FacultyServiceDep,
) -> Response:
    faculty = await faculty_service.get_by_id(faculty_id)
    if faculty is None or faculty.uni_id != university_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Faculty or university not found',
        )
    deleted_faculty = await faculty_service.delete(faculty_id)
    if deleted_faculty is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Faculty or university not found',
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
