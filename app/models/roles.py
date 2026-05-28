from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.users import UserModel


class UserRoleLink(SQLModel, table=True):
    __tablename__ = 'user_role_links'

    user_id: int = Field(foreign_key='users.id', primary_key=True)
    role_id: int = Field(foreign_key='roles.id', primary_key=True)


class RolePermissionLink(SQLModel, table=True):
    __tablename__ = 'role_permission_links'

    role_id: int = Field(foreign_key='roles.id', primary_key=True)
    permission_id: int = Field(foreign_key='permissions.id', primary_key=True)


class RoleBase(SQLModel):
    name: str = Field(index=True, unique=True, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class PermissionBase(SQLModel):
    scope: str = Field(index=True, unique=True, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class RoleModel(RoleBase, IDModel, TimestampedModel, table=True):
    __tablename__ = 'roles'

    users: list['UserModel'] = Relationship(
        back_populates='roles',
        link_model=UserRoleLink,
    )
    permissions: list['PermissionModel'] = Relationship(
        back_populates='roles',
        link_model=RolePermissionLink,
    )


class PermissionModel(PermissionBase, IDModel, TimestampedModel, table=True):
    __tablename__ = 'permissions'

    roles: list['RoleModel'] = Relationship(
        back_populates='permissions',
        link_model=RolePermissionLink,
    )