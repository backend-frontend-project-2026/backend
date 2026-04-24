from fastapi import APIRouter, HTTPException, Query, Response, status

from app.dependencies.services import (
    DormServiceDep,
    FacultyServiceDep,
    UniversityServiceDep,
)
from app.schemas.dorms import (
    DormCreate,
    DormFilters,
    DormListResponse,
    DormResponse,
    DormUpdate,
)
from app.schemas.faculties import (
    FacultyCreate,
    FacultyFilters,
    FacultyListResponse,
    FacultyResponse,
    FacultyUpdate,
)
from app.schemas.universities import (
    UniversityCreate,
    UniversityFilters,
    UniversityListResponse,
    UniversityResponse,
    UniversityUpdate,
)

router = APIRouter(prefix='/universities', tags=['Universities'])
faculty_router = APIRouter(
    prefix='/universities/{university_id}/faculties',
    tags=['Faculties'],
)
dorm_router = APIRouter(
    prefix='/universities/{university_id}/dorms',
    tags=['Dorms'],
)


@router.get('', response_model=UniversityListResponse)
async def list_universities(
    university_service: UniversityServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    name: str | None = None,
    city: str | None = None,
) -> UniversityListResponse:
    return await university_service.get_list(
        UniversityFilters(page=page, page_size=page_size, name=name, city=city)
    )


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


@faculty_router.get('', response_model=FacultyListResponse)
async def list_faculties(
    university_id: int,
    faculty_service: FacultyServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    name: str | None = None,
) -> FacultyListResponse:
    return await faculty_service.get_list(
        FacultyFilters(page=page, page_size=page_size, name=name, uni_id=university_id)
    )


@faculty_router.post('', response_model=FacultyResponse, status_code=status.HTTP_201_CREATED)
async def create_faculty(
    university_id: int,
    faculty_create: FacultyCreate,
    faculty_service: FacultyServiceDep,
) -> FacultyResponse:
    return await faculty_service.create(
        faculty_create.model_copy(update={'uni_id': university_id})
    )


@faculty_router.get('/{faculty_id}', response_model=FacultyResponse)
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


@faculty_router.put('/{faculty_id}', response_model=FacultyResponse)
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
        faculty_update.model_copy(update={'uni_id': university_id}),
    )
    if faculty is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Faculty or university not found',
        )
    return faculty


@faculty_router.delete('/{faculty_id}', status_code=status.HTTP_204_NO_CONTENT)
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


@dorm_router.get('', response_model=DormListResponse)
async def list_dorms(
    university_id: int,
    dorm_service: DormServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    name: str | None = None,
    city: str | None = None,
) -> DormListResponse:
    return await dorm_service.get_list(
        DormFilters(
            page=page, page_size=page_size, name=name, city=city, uni_id=university_id
        )
    )


@dorm_router.post('', response_model=DormResponse, status_code=status.HTTP_201_CREATED)
async def create_dorm(
    university_id: int,
    dorm_create: DormCreate,
    dorm_service: DormServiceDep,
) -> DormResponse:
    return await dorm_service.create(
        dorm_create.model_copy(update={'uni_id': university_id})
    )


@dorm_router.get('/{dorm_id}', response_model=DormResponse)
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


@dorm_router.put('/{dorm_id}', response_model=DormResponse)
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
        dorm_update.model_copy(update={'uni_id': university_id}),
    )
    if dorm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Dorm or university not found'
        )
    return dorm


@dorm_router.delete('/{dorm_id}', status_code=status.HTTP_204_NO_CONTENT)
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
