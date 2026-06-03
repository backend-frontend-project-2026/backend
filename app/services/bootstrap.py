from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.models.roles import (
    PermissionModel,
    RoleModel,
    RolePermissionLink,
    UserRoleLink,
)
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
    permissions_by_scope = await _ensure_permissions(session)
    roles_by_name = await _ensure_roles(session)

    await _sync_role_permissions(
        session=session,
        roles_by_name=roles_by_name,
        permissions_by_scope=permissions_by_scope,
    )

    await _bootstrap_admin_user(session, roles_by_name)

    await session.commit()


async def _ensure_permissions(
    session: AsyncSession,
) -> dict[str, PermissionModel]:
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
            await session.flush()

        permissions_by_scope[scope] = permission

    return permissions_by_scope


async def _ensure_roles(session: AsyncSession) -> dict[str, RoleModel]:
    roles_by_name: dict[str, RoleModel] = {}

    for role_name in ROLE_PERMISSIONS:
        result = await session.execute(
            select(RoleModel).where(RoleModel.name == role_name)
        )
        role = result.scalars().first()

        if role is None:
            role = RoleModel(name=role_name)
            session.add(role)
            await session.flush()

        roles_by_name[role_name] = role

    return roles_by_name


async def _sync_role_permissions(
    session: AsyncSession,
    roles_by_name: dict[str, RoleModel],
    permissions_by_scope: dict[str, PermissionModel],
) -> None:
    for role_name, scopes in ROLE_PERMISSIONS.items():
        role = roles_by_name[role_name]

        await session.execute(
            delete(RolePermissionLink).where(
                RolePermissionLink.role_id == role.id,
            )
        )

        for scope in scopes:
            permission = permissions_by_scope[scope]
            session.add(
                RolePermissionLink(
                    role_id=role.id,
                    permission_id=permission.id,
                )
            )

    await session.flush()


async def _bootstrap_admin_user(
    session: AsyncSession,
    roles_by_name: dict[str, RoleModel],
) -> None:
    result = await session.execute(
        select(UserModel).where(UserModel.email == settings.RBAC_ADMIN_EMAIL)
    )
    admin_user = result.scalars().first()

    admin_role = roles_by_name.get(settings.RBAC_ADMIN_ROLE)
    if admin_role is None:
        return

    if admin_user is None:
        admin_user = UserModel(
            first_name=settings.RBAC_ADMIN_FIRST_NAME,
            last_name=settings.RBAC_ADMIN_LAST_NAME,
            email=settings.RBAC_ADMIN_EMAIL,
            password_hash=get_password_hash(settings.RBAC_ADMIN_PASSWORD),
        )
        session.add(admin_user)
        await session.flush()

    await session.execute(
        delete(UserRoleLink).where(UserRoleLink.user_id == admin_user.id)
    )
    session.add(
        UserRoleLink(
            user_id=admin_user.id,
            role_id=admin_role.id,
        )
    )

    await session.flush()
