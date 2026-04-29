from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies.services import ReactionServiceDep
from app.schemas.reactions import (
    ReactionCreate,
    ReactionFilters,
    ReactionListResponse,
    ReactionResponse,
)

router = APIRouter(prefix='/deals/{deal_id}/reactions', tags=['Reactions'])


@router.get('')
async def list_reactions(
    reaction_service: ReactionServiceDep,
    filters: Annotated[ReactionFilters, Depends()],
) -> ReactionListResponse:
    return await reaction_service.get_list(filters)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_reaction(
    deal_id: int,
    reaction_create: ReactionCreate,
    reaction_service: ReactionServiceDep,
) -> ReactionResponse:
    return await reaction_service.create(reaction_create, deal_id=deal_id)


@router.get('/{reaction_id}')
async def get_reaction(
    deal_id: int,
    reaction_id: int,
    reaction_service: ReactionServiceDep,
) -> ReactionResponse:
    reaction = await reaction_service.get_reaction(deal_id, reaction_id)
    if reaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return reaction


@router.delete('/{reaction_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_reaction(
    deal_id: int,
    reaction_id: int,
    reaction_service: ReactionServiceDep,
) -> Response:
    reaction = await reaction_service.delete_reaction(deal_id, reaction_id)
    if reaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
