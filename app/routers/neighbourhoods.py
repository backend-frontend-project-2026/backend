from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies.services import NeighbourhoodServiceDep
from app.schemas.neighbourhoods import (
    NeighbourhoodCreate,
    NeighbourhoodFilters,
    NeighbourhoodListResponse,
    NeighbourhoodResponse,
    NeighbourhoodUpdate,
)

router = APIRouter(prefix='/neighbourhoods', tags=['Neighbourhoods'])


@router.get('', response_model=NeighbourhoodListResponse)
async def list_neighbourhoods(
    neighbourhood_service: NeighbourhoodServiceDep,
    filters: Annotated[NeighbourhoodFilters, Depends()],
) -> NeighbourhoodListResponse:
    return await neighbourhood_service.get_list(filters)


@router.get('/{neighbourhood_id}', response_model=NeighbourhoodResponse)
async def get_neighbourhood(
    neighbourhood_id: int,
    neighbourhood_service: NeighbourhoodServiceDep,
) -> NeighbourhoodResponse:
    neighbourhood = await neighbourhood_service.get_by_id(neighbourhood_id)
    if neighbourhood is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return neighbourhood


@router.post(
    '',
    response_model=NeighbourhoodResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_neighbourhood(
    neighbourhood_create: NeighbourhoodCreate,
    neighbourhood_service: NeighbourhoodServiceDep,
) -> NeighbourhoodResponse:
    return await neighbourhood_service.create(neighbourhood_create)


@router.put('/{neighbourhood_id}', response_model=NeighbourhoodResponse)
async def update_neighbourhood(
    neighbourhood_id: int,
    neighbourhood_update: NeighbourhoodUpdate,
    neighbourhood_service: NeighbourhoodServiceDep,
) -> NeighbourhoodResponse:
    neighbourhood = await neighbourhood_service.update(
        neighbourhood_id, neighbourhood_update
    )
    if neighbourhood is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return neighbourhood


@router.delete('/{neighbourhood_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_neighbourhood(
    neighbourhood_id: int,
    neighbourhood_service: NeighbourhoodServiceDep,
) -> Response:
    neighbourhood = await neighbourhood_service.delete(neighbourhood_id)
    if neighbourhood is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
