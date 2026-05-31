from typing import Any, Optional

from app.dependencies.repositories import UserRepository, UserRepositoryDep
from app.models.users import UserCreate, UserModel, UserUpdate
from app.schemas.users import (
    UserFilters,
    UserListResponse,
    UserPublic,
)
from app.services.crud import CrudService
from app.utils.hashing import get_password_hash


class UserService(CrudService):
    __user_repository: UserRepository

    def __init__(self, user_repository: UserRepositoryDep):
        super().__init__(user_repository, UserPublic, UserListResponse)
        self.__user_repository = user_repository

    def _prepare_create_data(
        self, payload: UserCreate, **extra_data: Any
    ) -> dict[str, Any]:
        user_data = super()._prepare_create_data(payload, **extra_data)
        password = user_data.pop('password')
        user_data['password_hash'] = get_password_hash(str(password))
        return user_data

    def _prepare_update_data(self, payload: UserUpdate) -> dict[str, Any]:
        update_dump = super()._prepare_update_data(payload)
        password = update_dump.pop('password', None)
        if password is not None:
            update_dump['password_hash'] = get_password_hash(str(password))
        return update_dump

    async def _get_user_model_by_email(self, email: str) -> Optional[UserModel]:
        users = await self.__user_repository.fetch(filters=UserFilters(email=email))
        if len(users) != 1:
            return None
        return users[0]

    async def get_user_by_email(self, email: str) -> Optional[UserPublic]:
        user = await self._get_user_model_by_email(email)
        return self._to_response(user) if user is not None else None

    async def update_user(
        self, user_update: UserUpdate, user_id: int
    ) -> Optional[UserPublic]:
        return await super().update(user_id, user_update)
