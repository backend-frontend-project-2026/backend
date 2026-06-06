from fastapi import APIRouter, Security

from app.dependencies.auth import get_current_user
from app.exceptions.responses import common_error_responses
from app.models.users import UserModel
from app.schemas.references import ReferenceListResponse, ReferenceOption

router = APIRouter(prefix='/references', tags=['References'])

_HOUSING_TYPES: list[dict[str, str]] = [
    {'value': 'dormitory', 'label': 'Общежитие'},
    {'value': 'rental', 'label': 'Съёмная квартира'},
]


@router.get(
    '/housing-types',
    response_model=ReferenceListResponse,
    responses=common_error_responses,
)
async def get_references_housing_types(
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:read'],
    ),
) -> ReferenceListResponse:
    return ReferenceListResponse(
        items=[
            ReferenceOption(**housing_type)
            for housing_type in _HOUSING_TYPES
        ]
    )
