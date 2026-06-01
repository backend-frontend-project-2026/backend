from typing import Optional

from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.roles import (
    PermissionModel,
    RoleModel,
    RolePermissionLink,
    UserRoleLink,
)
from app.models.users import UserModel
from app.schemas.roles import (
    PermissionFilters,
    PermissionListResponse,
    PermissionResponse,
    RoleCreate,
    RoleFilters,
    RoleListResponse,
    RoleResponse,
    RoleUpdate,
)


class RoleService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_roles(self, filters: RoleFilters) -> RoleListResponse:
        stmt = select(RoleModel)
        if filters.name:
            stmt = stmt.where(RoleModel.name == filters.name)
        result = await self._session.execute(
            stmt.offset(filters.offset).limit(filters.limit)
        )
        roles = result.scalars().all()
        total_result = await self._session.execute(select(RoleModel))
        total = len(total_result.scalars().all())
        return RoleListResponse(
            items=[self._role_to_response(r) for r in roles],
            total=total,
            page=filters.page,
            page_size=filters.page_size,
        )

    async def get_role(self, role_id: int) -> Optional[RoleResponse]:
        role = await self._session.get(RoleModel, role_id)
        if role is None:
            return None
        return self._role_to_response(role)

    async def create_role(self, payload: RoleCreate) -> RoleResponse:
        role = RoleModel(name=payload.name)
        self._session.add(role)
        await self._session.flush()

        for scope in payload.scope_aliases:
            permission = await self._get_or_create_permission(scope)
            self._session.add(
                RolePermissionLink(role_id=role.id, permission_id=permission.id)
            )

        await self._session.commit()
        await self._session.refresh(role)
        return self._role_to_response(role)

    async def update_role(
        self, role_id: int, payload: RoleUpdate
    ) -> Optional[RoleResponse]:
        role = await self._session.get(RoleModel, role_id)
        if role is None:
            return None

        if payload.name is not None:
            role.name = payload.name

        if payload.scope_aliases is not None:
            links_result = await self._session.execute(
                select(RolePermissionLink).where(
                    RolePermissionLink.role_id == role_id
                )
            )
            for link in links_result.scalars().all():
                await self._session.delete(link)
            await self._session.flush()

            for scope in payload.scope_aliases:
                permission = await self._get_or_create_permission(scope)
                self._session.add(
                    RolePermissionLink(role_id=role.id, permission_id=permission.id)
                )

        self._session.add(role)
        await self._session.commit()
        await self._session.refresh(role)
        return self._role_to_response(role)

    async def delete_role(self, role_id: int) -> Optional[RoleResponse]:
        role = await self._session.get(RoleModel, role_id)
        if role is None:
            return None
        response = self._role_to_response(role)
        await self._session.delete(role)
        await self._session.commit()
        return response

    async def get_permissions(
        self, filters: PermissionFilters
    ) -> PermissionListResponse:
        stmt = select(PermissionModel)
        if filters.scope:
            stmt = stmt.where(PermissionModel.scope == filters.scope)
        result = await self._session.execute(
            stmt.offset(filters.offset).limit(filters.limit)
        )
        permissions = result.scalars().all()
        total_result = await self._session.execute(select(PermissionModel))
        total = len(total_result.scalars().all())
        return PermissionListResponse(
            items=[self._permission_to_response(p) for p in permissions],
            total=total,
            page=filters.page,
            page_size=filters.page_size,
        )

    async def assign_roles_to_user(
        self, user_id: int, role_ids: list[int]
    ) -> Optional[UserModel]:
        user = await self._session.get(UserModel, user_id)
        if user is None:
            return None

        existing_result = await self._session.execute(
            select(UserRoleLink).where(UserRoleLink.user_id == user_id)
        )
        for link in existing_result.scalars().all():
            await self._session.delete(link)
        await self._session.flush()

        for role_id in role_ids:
            role = await self._session.get(RoleModel, role_id)
            if role is not None:
                self._session.add(
                    UserRoleLink(user_id=user_id, role_id=role_id)
                )

        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def _get_or_create_permission(self, scope: str) -> PermissionModel:
        result = await self._session.execute(
            select(PermissionModel).where(PermissionModel.scope == scope)
        )
        permission = result.scalars().first()
        if permission is None:
            permission = PermissionModel(scope=scope)
            self._session.add(permission)
            await self._session.flush()
        return permission

    @staticmethod
    def _role_to_response(role: RoleModel) -> RoleResponse:
        return RoleResponse(
            id=role.id,
            name=role.name,
            scopes=role.scopes,
        )

    @staticmethod
    def _permission_to_response(permission: PermissionModel) -> PermissionResponse:
        return PermissionResponse(
            id=permission.id,
            scope=permission.scope,
        )
