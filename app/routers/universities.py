from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import UniversityServiceDep
from app.models.universities import UniversityCreate, UniversityUpdate
from app.models.users import UserModel
from app.schemas.universities import (
    UniversityFilters,
    UniversityListResponse,
    UniversityResponse,
)

router = APIRouter(prefix='/universities', tags=['Universities'])


@router.get('', response_model=UniversityListResponse)
async def list_universities(
    university_service: UniversityServiceDep,
    filters: Annotated[UniversityFilters, Depends()],
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:read'],
    ),
):
    return await university_service.get_list(filters)


@router.post('', response_model=UniversityResponse)
async def create_university(
    university_create: UniversityCreate,
    university_service: UniversityServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:create'],
    ),
):
    return await university_service.create(university_create)


@router.get('/{university_id}', response_model=UniversityResponse)
async def get_university(
    university_id: int,
    university_service: UniversityServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:read'],
    ),
):
    university = await university_service.get_by_id(university_id)
    if university is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='University not found',
        )
    return university


@router.put('/{university_id}', response_model=UniversityResponse)
async def update_university(
    university_id: int,
    university_update: UniversityUpdate,
    university_service: UniversityServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:update'],
    ),
):
    university = await university_service.update(university_id, university_update)
    if university is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='University not found',
        )
    return university


@router.delete('/{university_id}', response_model=UniversityResponse)
async def delete_university(
    university_id: int,
    university_service: UniversityServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:delete'],
    ),
):
    university = await university_service.delete(university_id)
    if university is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='University not found',
        )
    return university