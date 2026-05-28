from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.roles import PermissionModel, RoleModel

PUBLIC_ROLE_NAME = 'public'
ADMIN_ROLE_NAME = 'admin'

ROLE_PERMISSIONS = {
    PUBLIC_ROLE_NAME: [
        'auth:me',
        'profiles:read',
        'profiles:create',
        'profiles:update',
        'chats:read',
        'chats:create',
        'messages:read',
        'messages:create',
        'deals:read',
        'deals:create',
        'complaints:create',
        'references:read',
    ],
    ADMIN_ROLE_NAME: [
        'auth:me',
        'users:read',
        'users:create',
        'users:update',
        'users:delete',
        'profiles:read',
        'profiles:create',
        'profiles:update',
        'profiles:delete',
        'chats:read',
        'chats:create',
        'chats:delete',
        'messages:read',
        'messages:create',
        'messages:update',
        'messages:delete',
        'deals:read',
        'deals:create',
        'deals:update',
        'deals:delete',
        'complaints:read',
        'complaints:create',
        'complaints:update',
        'complaints:delete',
        'references:read',
        'references:create',
        'references:update',
        'references:delete',
    ],
}


async def bootstrap_roles_and_permissions(session: AsyncSession) -> None:
    permissions_by_scope: dict[str, PermissionModel] = {}

    all_scopes = sorted(
        {
            scope
            for scopes in ROLE_PERMISSIONS.values()
            for scope in scopes
        }
    )

    for scope in all_scopes:
        result = await session.execute(
            select(PermissionModel).where(PermissionModel.scope == scope)
        )
        permission = result.scalars().first()

        if permission is None:
            permission = PermissionModel(scope=scope)
            session.add(permission)

        permissions_by_scope[scope] = permission

    await session.flush()

    for role_name, scopes in ROLE_PERMISSIONS.items():
        result = await session.execute(
            select(RoleModel)
            .options(selectinload(RoleModel.permissions))
            .where(RoleModel.name == role_name)
        )
        role = result.scalars().first()

        if role is None:
            role = RoleModel(name=role_name)
            session.add(role)
            await session.flush()

        role.permissions = [permissions_by_scope[scope] for scope in scopes]

    await session.commit()