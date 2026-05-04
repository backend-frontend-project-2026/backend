from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies.services import FacultyServiceDep
from app.models.faculties import FacultyCreate, FacultyUpdate
from app.schemas.faculties import (
    FacultyFilters,
    FacultyListResponse,
    FacultyResponse,
)

router = APIRouter(prefix='/universities/{university_id}/faculties', tags=['Faculties'])


@router.get('', response_model=FacultyListResponse)
async def list_faculties(
    faculty_service: FacultyServiceDep,
    filters: Annotated[FacultyFilters, Depends()],
):
    return await faculty_service.get_list(filters)


@router.post('', response_model=FacultyResponse)
async def create_faculty(
    university_id: int,
    faculty_create: FacultyCreate,
    faculty_service: FacultyServiceDep,
):
    return await faculty_service.create(faculty_create, uni_id=university_id)


@router.get('/{faculty_id}', response_model=FacultyResponse)
async def get_faculty(
    university_id: int,
    faculty_id: int,
    faculty_service: FacultyServiceDep,
):
    faculty = await faculty_service.get_by_id(faculty_id)
    if faculty is None or faculty.uni_id != university_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Faculty or university not found',
        )
    return faculty


@router.put('/{faculty_id}', response_model=FacultyResponse)
async def update_faculty(
    university_id: int,
    faculty_id: int,
    faculty_update: FacultyUpdate,
    faculty_service: FacultyServiceDep,
):
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


@router.delete('/{faculty_id}', response_model=FacultyResponse)
async def delete_faculty(
    university_id: int,
    faculty_id: int,
    faculty_service: FacultyServiceDep,
):
    deleted_faculty = await faculty_service.delete(faculty_id)
    if deleted_faculty is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Faculty or university not found',
        )
    return deleted_faculty
