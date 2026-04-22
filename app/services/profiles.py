from typing import Optional

from app.dependencies.repositories import ProfileRepository, ProfileRepositoryDep
from app.models.profiles import ProfileModel
from app.schemas.profiles import (
    ProfileCreate,
    ProfileFilters,
    ProfileListResponse,
    ProfileResponse,
    ProfileUpdate,
)


class ProfileService:
    __profile_repository: ProfileRepository

    def __init__(self, profile_repository: ProfileRepositoryDep):
        self.__profile_repository = profile_repository

    def _to_response(self, profile: ProfileModel) -> ProfileResponse:
        return ProfileResponse.model_validate(profile)

    async def get_profiles(self, filters: ProfileFilters) -> ProfileListResponse:
        profiles = await self.__profile_repository.fetch(
            filters=filters,
            offset=filters.offset,
            limit=filters.limit,
        )
        total = await self.__profile_repository.count(filters=filters)
        return ProfileListResponse(
            items=[self._to_response(profile) for profile in profiles],
            total=total,
            page=filters.page,
            page_size=filters.page_size,
        )

    async def get_profile_by_user_id(self, user_id: int) -> Optional[ProfileResponse]:
        profiles = await self.__profile_repository.fetch(
            filters=ProfileFilters(user_id=user_id)
        )
        return self._to_response(profiles[0]) if profiles else None

    async def create_profile(
        self, user_id: int, profile_create: ProfileCreate
    ) -> ProfileResponse:
        profile = ProfileModel(
            user_id=user_id,
            **profile_create.model_dump(exclude_none=True),
        )
        saved_profile = await self.__profile_repository.save(profile)
        return self._to_response(saved_profile)

    async def update_profile(
        self, user_id: int, profile_update: ProfileUpdate
    ) -> Optional[ProfileResponse]:
        profiles = await self.__profile_repository.fetch(
            filters=ProfileFilters(user_id=user_id)
        )
        target_profile = profiles[0] if profiles else None
        if target_profile is None:
            return None

        for key, value in profile_update.model_dump(exclude_unset=True).items():
            if hasattr(target_profile, key):
                setattr(target_profile, key, value)

        saved_profile = await self.__profile_repository.save(target_profile)
        return self._to_response(saved_profile)

    async def delete_profile(self, user_id: int) -> Optional[ProfileResponse]:
        profiles = await self.__profile_repository.fetch(
            filters=ProfileFilters(user_id=user_id)
        )
        target_profile = profiles[0] if profiles else None
        if target_profile is None:
            return None
        await self.__profile_repository.delete(target_profile.id)
        return self._to_response(target_profile)
