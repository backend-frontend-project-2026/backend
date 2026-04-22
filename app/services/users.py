from typing import Optional

from app.dependencies.repositories import UserRepository, UserRepositoryDep
from app.models.users import UserModel
from app.schemas.users import UserFilters, UserListResponse, UserResponse, UserUpdate
from app.utils.hashing import get_password_hash


class UserService:
    __user_repository: UserRepository

    def __init__(self, user_repository: UserRepositoryDep):
        self.__user_repository = user_repository

    def _to_response(self, user: UserModel) -> UserResponse:
        return UserResponse.model_validate(user)

    async def get_users(self, filters: UserFilters) -> UserListResponse:
        users = await self.__user_repository.fetch(
            filters=filters,
            offset=filters.offset,
            limit=filters.limit,
        )
        total = await self.__user_repository.count(filters=filters)
        return UserListResponse(
            items=[self._to_response(user) for user in users],
            total=total,
            page=filters.page,
            page_size=filters.page_size,
        )

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        users = await self.__user_repository.fetch(filters=UserFilters(email=email))
        if len(users) != 1:
            return None
        return self._to_response(users[0])

    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        user = await self.__user_repository.get(user_id)
        if user is None:
            return None
        return self._to_response(user)

    async def update_user(
        self, user_update: UserUpdate, user_id: int
    ) -> Optional[UserResponse]:
        user = await self.__user_repository.get(user_id)
        if user is None:
            return None

        update_dump = user_update.model_dump(exclude_unset=True)
        password = update_dump.pop('password', None)
        if password is not None:
            update_dump['password_hash'] = get_password_hash(str(password))

        for key, value in update_dump.items():
            if hasattr(user, key):
                setattr(user, key, value)

        saved_user = await self.__user_repository.save(user)
        return self._to_response(saved_user)

    async def delete_user(self, user_id: int) -> Optional[UserResponse]:
        user = await self.__user_repository.delete(user_id)
        if user is None:
            return None
        return self._to_response(user)
