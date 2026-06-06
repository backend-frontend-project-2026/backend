from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/references', tags=['References'])


class ReferenceItem(BaseModel):
    value: str
    label: str


class ReferenceListResponse(BaseModel):
    items: list[ReferenceItem]


@router.get('/housing-types', response_model=ReferenceListResponse)
async def get_housing_types() -> ReferenceListResponse:
    return ReferenceListResponse(
        items=[
            ReferenceItem(value='dormitory', label='Общежитие'),
            ReferenceItem(value='rental', label='Съёмная квартира'),
        ],
    )