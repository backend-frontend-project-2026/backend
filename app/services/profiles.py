from typing import Optional

from app.dependencies.repositories import ProfileRepository, ProfileRepositoryDep
from app.models.profiles import ProfileModel, ProfileUpdate
from app.schemas.profiles import (
    ProfileFilters,
    ProfileListResponse,
    ProfileResponse,
)
from app.services.crud import CrudService


class ProfileService(CrudService):
    __profile_repository: ProfileRepository

    def __init__(self, profile_repository: ProfileRepositoryDep):
        super().__init__(profile_repository, ProfileResponse, ProfileListResponse)
        self.__profile_repository = profile_repository

    async def _get_profile_model_by_user_id(
        self, user_id: int
    ) -> Optional[ProfileModel]:
        profiles = await self.__profile_repository.fetch(
            filters=ProfileFilters(user_id=user_id)
        )
        return profiles[0] if profiles else None

    async def get_profile_by_user_id(self, user_id: int) -> Optional[ProfileResponse]:
        profile = await self._get_profile_model_by_user_id(user_id)
        return self._to_response(profile) if profile is not None else None

    async def update_profile(
        self, user_id: int, profile_update: ProfileUpdate
    ) -> Optional[ProfileResponse]:
        profile = await self._get_profile_model_by_user_id(user_id)
        if profile is None:
            return None
        return await super().update(profile.id, profile_update)

    async def delete_profile(self, user_id: int) -> Optional[ProfileResponse]:
        profile = await self._get_profile_model_by_user_id(user_id)
        if profile is None:
            return None
        return await super().delete(profile.id)
