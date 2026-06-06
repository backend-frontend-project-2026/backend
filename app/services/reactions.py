from typing import Any, Optional

from sqlmodel import select

from app.dependencies.repositories import (
    DealRepository,
    DealRepositoryDep,
    ReactionRepository,
    ReactionRepositoryDep,
)
from app.models.deals import DealModel
from app.models.reactions import ReactionCreate, ReactionModel, ReactionType
from app.schemas.reactions import (
    ReactionCreateResponse,
    ReactionListResponse,
    ReactionResponse,
)
from app.services.crud import CrudService


class ReactionService(CrudService):
    __reaction_repository: ReactionRepository
    __deal_repository: DealRepository

    def __init__(
        self,
        reaction_repository: ReactionRepositoryDep,
        deal_repository: DealRepositoryDep,
    ):
        super().__init__(reaction_repository, ReactionResponse, ReactionListResponse)
        self.__reaction_repository = reaction_repository
        self.__deal_repository = deal_repository

    async def _check_mutual(
        self, profile_id: int, deal_owner_profile_id: int
    ) -> bool:
        stmt = (
            select(ReactionModel)
            .join(DealModel, ReactionModel.deal_id == DealModel.id)
            .where(
                ReactionModel.profile_id == deal_owner_profile_id,
                DealModel.owner_profile_id == profile_id,
                ReactionModel.reaction_type == ReactionType.LIKE,
            )
            .limit(1)
        )
        result = await self.__reaction_repository.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def create(
        self, payload: ReactionCreate, **extra_data: Any
    ) -> ReactionCreateResponse:
        reaction = await super().create(payload, **extra_data)
        deal = await self.__deal_repository.get(extra_data['deal_id'])

        mutual = False
        if deal is not None and payload.reaction_type == ReactionType.LIKE:
            mutual = await self._check_mutual(payload.profile_id, deal.owner_profile_id)

        return ReactionCreateResponse(**reaction.model_dump(), mutual=mutual)

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
