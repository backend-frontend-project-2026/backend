from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.services import DealServiceDep
from app.models.deals import DealCreate
from app.schemas.deals import (
    DealFilters,
    DealListResponse,
    DealResponse,
)

router = APIRouter(prefix='/deals', tags=['Deals'])


@router.get('', response_model=DealListResponse)
async def list_deals(
    deal_service: DealServiceDep,
    filters: Annotated[DealFilters, Depends()],
):
    return await deal_service.get_list(filters)


@router.post('', response_model=DealResponse)
async def create_deal(
    deal_create: DealCreate,
    deal_service: DealServiceDep,
):
    return await deal_service.create(deal_create)


@router.get('/{deal_id}', response_model=DealResponse)
async def get_deal(
    deal_id: int,
    deal_service: DealServiceDep,
):
    deal = await deal_service.get_by_id(deal_id)
    if deal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Deal not found'
        )
    return deal
