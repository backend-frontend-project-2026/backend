from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies.services import ReactionServiceDep
from app.models.reactions import ReactionCreate
from app.schemas.reactions import (
    ReactionFilters,
    ReactionListResponse,
    ReactionResponse,
)

router = APIRouter(prefix='/deals/{deal_id}/reactions', tags=['Reactions'])


@router.get('', response_model=ReactionListResponse)
async def list_reactions(
    reaction_service: ReactionServiceDep,
    filters: Annotated[ReactionFilters, Depends()],
):
    return await reaction_service.get_list(filters)


@router.post('', response_model=ReactionResponse)
async def create_reaction(
    deal_id: int,
    reaction_create: ReactionCreate,
    reaction_service: ReactionServiceDep,
):
    return await reaction_service.create(reaction_create, deal_id=deal_id)


@router.get('/{reaction_id}', response_model=ReactionResponse)
async def get_reaction(
    deal_id: int,
    reaction_id: int,
    reaction_service: ReactionServiceDep,
):
    reaction = await reaction_service.get_reaction(deal_id, reaction_id)
    if reaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return reaction


@router.delete('/{reaction_id}', response_model=ReactionResponse)
async def delete_reaction(
    deal_id: int,
    reaction_id: int,
    reaction_service: ReactionServiceDep,
):
    reaction = await reaction_service.delete_reaction(deal_id, reaction_id)
    if reaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return reaction
