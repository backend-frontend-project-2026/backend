from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.dependencies.services import DealServiceDep, ReactionServiceDep
from app.schemas.deals import (
    DealCreate,
    DealFilters,
    DealListResponse,
    DealResponse,
    DealType,
)
from app.schemas.reactions import (
    ReactionCreate,
    ReactionFilters,
    ReactionListResponse,
    ReactionResponse,
    ReactionType,
)

router = APIRouter(prefix='/deals', tags=['Deals'])
reaction_router = APIRouter(prefix='/deals/{deal_id}/reactions', tags=['Reactions'])


@router.get('', response_model=DealListResponse)
async def list_deals(
    deal_service: DealServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    city: str | None = None,
    deal_type: DealType | None = None,
    budget_min: int | None = None,
    budget_max: int | None = None,
    people_amount: int | None = None,
    neighbourhood_id: int | None = None,
) -> DealListResponse:
    return await deal_service.get_list(
        DealFilters(
            page=page,
            page_size=page_size,
            city=city,
            deal_type=deal_type,
            budget_min=budget_min,
            budget_max=budget_max,
            people_amount=people_amount,
            neighbourhood_id=neighbourhood_id,
        )
    )


@router.post('', response_model=DealResponse, status_code=status.HTTP_201_CREATED)
async def create_deal(
    deal_create: DealCreate,
    deal_service: DealServiceDep,
) -> DealResponse:
    return await deal_service.create(deal_create)


@router.get('/{deal_id}', response_model=DealResponse)
async def get_deal(
    deal_id: int,
    deal_service: DealServiceDep,
) -> DealResponse:
    deal = await deal_service.get_by_id(deal_id)
    if deal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Deal not found'
        )
    return deal


@reaction_router.get('', response_model=ReactionListResponse)
async def list_reactions(
    deal_id: int,
    reaction_service: ReactionServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    reaction_type: ReactionType | None = None,
    profile_id: int | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
) -> ReactionListResponse:
    return await reaction_service.get_reactions(
        deal_id,
        ReactionFilters(
            page=page,
            page_size=page_size,
            deal_id=deal_id,
            reaction_type=reaction_type,
            profile_id=profile_id,
            created_from=created_from,
            created_to=created_to,
        ),
    )


@reaction_router.post('', response_model=ReactionResponse, status_code=status.HTTP_201_CREATED)
async def create_reaction(
    deal_id: int,
    reaction_create: ReactionCreate,
    reaction_service: ReactionServiceDep,
) -> ReactionResponse:
    return await reaction_service.create_reaction(deal_id, reaction_create)


@reaction_router.get('/{reaction_id}', response_model=ReactionResponse)
async def get_reaction(
    deal_id: int,
    reaction_id: int,
    reaction_service: ReactionServiceDep,
) -> ReactionResponse:
    reaction = await reaction_service.get_reaction(deal_id, reaction_id)
    if reaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return reaction


@reaction_router.delete('/{reaction_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_reaction(
    deal_id: int,
    reaction_id: int,
    reaction_service: ReactionServiceDep,
) -> Response:
    reaction = await reaction_service.delete_reaction(deal_id, reaction_id)
    if reaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
