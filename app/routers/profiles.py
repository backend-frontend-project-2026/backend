from fastapi import APIRouter, Query

from app.dependencies.services import ProfileServiceDep
from app.models.profiles import ProfileSex
from app.schemas.profiles import ProfileFilters, ProfileListResponse

router = APIRouter(prefix='/profiles', tags=['Profiles'])


@router.get('', response_model=ProfileListResponse)
async def list_profiles(
    profile_service: ProfileServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    sex: ProfileSex | None = None,
    age_min: int | None = None,
    age_max: int | None = None,
    uni_id: int | None = None,
    faculty_id: int | None = None,
    city: str | None = None,
    neighbourhood_id: int | None = None,
    tag_id: int | None = None,
    course: int | None = None,
) -> ProfileListResponse:
    filters = ProfileFilters(
        page=page,
        page_size=page_size,
        sex=sex,
        age_min=age_min,
        age_max=age_max,
        uni_id=uni_id,
        faculty_id=faculty_id,
        city=city,
        neighbourhood_id=neighbourhood_id,
        tag_id=tag_id,
        course=course,
    )
    return await profile_service.get_profiles(filters)
