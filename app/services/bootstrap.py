from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.models.roles import PermissionModel, RoleModel
from app.models.users import UserModel
from app.utils.hashing import get_password_hash

ROLE_PERMISSIONS = {
    settings.RBAC_PUBLIC_ROLE: [
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
    settings.RBAC_ADMIN_ROLE: [
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
        'roles:read',
        'roles:create',
        'roles:update',
        'roles:delete',
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

    await session.flush()

    await _bootstrap_admin_user(session, permissions_by_scope)

    await session.commit()


async def _bootstrap_admin_user(
    session: AsyncSession,
    permissions_by_scope: dict[str, PermissionModel],
) -> None:
    result = await session.execute(
        select(UserModel).where(UserModel.email == settings.RBAC_ADMIN_EMAIL)
    )
    if result.scalars().first() is not None:
        return

    admin_role_result = await session.execute(
        select(RoleModel).where(RoleModel.name == settings.RBAC_ADMIN_ROLE)
    )
    admin_role = admin_role_result.scalars().first()

    if admin_role is None:
        return

    admin_user = UserModel(
        first_name=settings.RBAC_ADMIN_FIRST_NAME,
        last_name=settings.RBAC_ADMIN_LAST_NAME,
        email=settings.RBAC_ADMIN_EMAIL,
        password_hash=get_password_hash(settings.RBAC_ADMIN_PASSWORD),
    )
    admin_user.roles = [admin_role]
    session.add(admin_user)
