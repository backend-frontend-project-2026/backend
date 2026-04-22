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


@router.get(
    '/{university_id}/faculties', response_model=FacultyListResponse, tags=['Faculties']
)
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


@router.post(
    '/{university_id}/faculties',
    response_model=FacultyResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Faculties'],
)
async def create_faculty(
    university_id: int,
    faculty_create: FacultyCreate,
    faculty_service: FacultyServiceDep,
) -> FacultyResponse:
    return await faculty_service.create(faculty_create)


@router.get(
    '/{university_id}/faculties/{faculty_id}',
    response_model=FacultyResponse,
    tags=['Faculties'],
)
async def get_faculty(
    university_id: int,
    faculty_id: int,
    faculty_service: FacultyServiceDep,
) -> FacultyResponse:
    faculty = await faculty_service.get_by_id(faculty_id)
    if faculty is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Faculty or university not found',
        )
    return faculty


@router.put(
    '/{university_id}/faculties/{faculty_id}',
    response_model=FacultyResponse,
    tags=['Faculties'],
)
async def update_faculty(
    university_id: int,
    faculty_id: int,
    faculty_update: FacultyUpdate,
    faculty_service: FacultyServiceDep,
) -> FacultyResponse:
    faculty = await faculty_service.update(faculty_id, faculty_update)
    if faculty is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Faculty or university not found',
        )
    return faculty


@router.delete(
    '/{university_id}/faculties/{faculty_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Faculties'],
)
async def delete_faculty(
    university_id: int,
    faculty_id: int,
    faculty_service: FacultyServiceDep,
) -> Response:
    faculty = await faculty_service.delete(faculty_id)
    if faculty is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Faculty or university not found',
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/{university_id}/dorms', response_model=DormListResponse, tags=['Dorms'])
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


@router.post(
    '/{university_id}/dorms',
    response_model=DormResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Dorms'],
)
async def create_dorm(
    university_id: int,
    dorm_create: DormCreate,
    dorm_service: DormServiceDep,
) -> DormResponse:
    return await dorm_service.create(dorm_create)


@router.get(
    '/{university_id}/dorms/{dorm_id}', response_model=DormResponse, tags=['Dorms']
)
async def get_dorm(
    university_id: int,
    dorm_id: int,
    dorm_service: DormServiceDep,
) -> DormResponse:
    dorm = await dorm_service.get_by_id(dorm_id)
    if dorm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Dorm or university not found'
        )
    return dorm


@router.put(
    '/{university_id}/dorms/{dorm_id}', response_model=DormResponse, tags=['Dorms']
)
async def update_dorm(
    university_id: int,
    dorm_id: int,
    dorm_update: DormUpdate,
    dorm_service: DormServiceDep,
) -> DormResponse:
    dorm = await dorm_service.update(dorm_id, dorm_update)
    if dorm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Dorm or university not found'
        )
    return dorm


@router.delete(
    '/{university_id}/dorms/{dorm_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Dorms'],
)
async def delete_dorm(
    university_id: int,
    dorm_id: int,
    dorm_service: DormServiceDep,
) -> Response:
    dorm = await dorm_service.delete(dorm_id)
    if dorm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Dorm or university not found'
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
