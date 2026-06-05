from typing import Annotated

from fastapi import APIRouter, Depends

from app.schemas.cities import CityFilters, CityListResponse, CityItem

router = APIRouter(prefix='/cities', tags=['Cities'])

_MOCK_CITIES = [
    CityItem(id=1, name='Казань'),
]


@router.get('', response_model=CityListResponse)
async def list_cities(filters: Annotated[CityFilters, Depends()]):
    filtered = _MOCK_CITIES
    if filters.name:
        filtered = [c for c in filtered if filters.name.lower() in c.name.lower()]

    start = filters.offset
    end = start + filters.limit
    return CityListResponse(
        items=filtered[start:end],
        total=len(filtered),
        page=filters.page,
        page_size=filters.page_size,
    )
