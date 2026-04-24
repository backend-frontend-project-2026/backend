from typing import Optional

from app.dependencies.repositories import ReactionRepository, ReactionRepositoryDep
from app.models.reactions import ReactionModel
from app.schemas.reactions import (
    ReactionCreate,
    ReactionFilters,
    ReactionListResponse,
    ReactionResponse,
)


class ReactionService:
    __reaction_repository: ReactionRepository

    def __init__(self, reaction_repository: ReactionRepositoryDep):
        self.__reaction_repository = reaction_repository

    def _to_response(self, reaction: ReactionModel) -> ReactionResponse:
        return ReactionResponse.model_validate(reaction)

    async def get_reactions(
        self, deal_id: int, filters: ReactionFilters
    ) -> ReactionListResponse:
        reactions = await self.__reaction_repository.fetch(
            filters=filters.model_copy(update={'deal_id': deal_id}),
            offset=filters.offset,
            limit=filters.limit,
        )
        total = await self.__reaction_repository.count(
            filters=filters.model_copy(update={'deal_id': deal_id})
        )
        return ReactionListResponse(
            items=[self._to_response(reaction) for reaction in reactions],
            total=total,
            page=filters.page,
            page_size=filters.page_size,
        )

    async def create_reaction(
        self, deal_id: int, reaction_create: ReactionCreate
    ) -> ReactionResponse:
        reaction = ReactionModel(
            deal_id=deal_id,
            **reaction_create.model_dump(exclude_none=True),
        )
        saved_reaction = await self.__reaction_repository.save(reaction)
        return self._to_response(saved_reaction)

    async def get_reaction(
        self, deal_id: int, reaction_id: int
    ) -> Optional[ReactionResponse]:
        reaction = await self.__reaction_repository.get(reaction_id)
        if reaction is None or reaction.deal_id != deal_id:
            return None
        return self._to_response(reaction)

    async def delete_reaction(
        self, deal_id: int, reaction_id: int
    ) -> Optional[ReactionResponse]:
        reaction = await self.__reaction_repository.get(reaction_id)
        if reaction is None or reaction.deal_id != deal_id:
            return None
        await self.__reaction_repository.delete(reaction_id)
        return self._to_response(reaction)
