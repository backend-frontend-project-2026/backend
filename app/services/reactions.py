from typing import Optional

from app.dependencies.repositories import ReactionRepository, ReactionRepositoryDep
from app.schemas.reactions import (
    ReactionListResponse,
    ReactionResponse,
)
from app.services.crud import CrudService


class ReactionService(CrudService):
    __reaction_repository: ReactionRepository

    def __init__(self, reaction_repository: ReactionRepositoryDep):
        super().__init__(reaction_repository, ReactionResponse, ReactionListResponse)
        self.__reaction_repository = reaction_repository

    async def _get_reaction_by_deal_id(
        self, deal_id: int, reaction_id: int
    ) -> Optional[ReactionResponse]:
        reaction = await super().get_by_id(reaction_id)
        if reaction is None or reaction.deal_id != deal_id:
            return None
        return reaction

    async def get_reaction(
        self, deal_id: int, reaction_id: int
    ) -> Optional[ReactionResponse]:
        return await self._get_reaction_by_deal_id(deal_id, reaction_id)

    async def delete_reaction(
        self, deal_id: int, reaction_id: int
    ) -> Optional[ReactionResponse]:
        reaction = await self._get_reaction_by_deal_id(deal_id, reaction_id)
        if reaction is None:
            return None
        await super().delete(reaction_id)
        return reaction
