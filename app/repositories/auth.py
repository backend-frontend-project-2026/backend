from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models.refresh_sessions import RefreshSessionModel
from app.models.roles import RoleModel
from app.models.users import UserModel
from app.utils.repository import Repository


class UserAuthRepository(Repository[UserModel]):
    async def get_by_email(self, email: str) -> Optional[UserModel]:
        result = await self._session.execute(
            select(UserModel)
            .options(
                selectinload(UserModel.roles).selectinload(RoleModel.permissions)
            )
            .where(UserModel.email == email)
        )
        return result.scalars().first()


class RefreshSessionRepository(Repository[RefreshSessionModel]):
    async def get_by_refresh_jti(
        self,
        refresh_jti: str,
    ) -> Optional[RefreshSessionModel]:
        result = await self._session.execute(
            select(RefreshSessionModel).where(
                RefreshSessionModel.refresh_token_jti == refresh_jti,
            )
        )
        return result.scalars().first()

    async def invalidate_all_by_user_id(self, user_id: int) -> None:
        result = await self._session.execute(
            select(RefreshSessionModel).where(
                RefreshSessionModel.user_id == user_id,
                RefreshSessionModel.is_invalidated.is_(False),
            )
        )
        refresh_sessions = result.scalars().all()

        for refresh_session in refresh_sessions:
            refresh_session.is_invalidated = True
            refresh_session.invalidated_at = datetime.now(timezone.utc)

        await self._session.commit()


class RoleRepository(Repository[RoleModel]):
    async def get_by_name(self, name: str) -> RoleModel | None:
        result = await self._session.execute(
            select(RoleModel)
            .options(selectinload(RoleModel.permissions))
            .where(RoleModel.name == name)
        )
        return result.scalars().first()