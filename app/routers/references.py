from fastapi import APIRouter

from app.schemas.references import ReferenceListResponse, ReferenceOption

router = APIRouter(prefix='/references', tags=['References'])

_HOUSING_TYPES: list[dict[str, str]] = [
    {'value': 'dormitory', 'label': 'Общежитие'},
    {'value': 'rental', 'label': 'Съёмная квартира'},
]


@router.get(
    '/housing-types',
    response_model=ReferenceListResponse,
)
async def get_references_housing_types():
    return ReferenceListResponse(items=[ReferenceOption(**h) for h in _HOUSING_TYPES])
