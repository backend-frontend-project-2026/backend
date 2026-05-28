"""add roles and permissions

Revision ID: 116692ea3208
Revises: dee830e54421
Create Date: 2026-05-28 13:59:29.565806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '116692ea3208'
down_revision: Union[str, Sequence[str], None] = 'dee830e54421'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'permissions',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column(
            'scope',
            sqlmodel.sql.sqltypes.AutoString(length=100),
            nullable=False,
        ),
        sa.Column(
            'description',
            sqlmodel.sql.sqltypes.AutoString(length=255),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_permissions_scope'),
        'permissions',
        ['scope'],
        unique=True,
    )

    op.create_table(
        'roles',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column(
            'name',
            sqlmodel.sql.sqltypes.AutoString(length=100),
            nullable=False,
        ),
        sa.Column(
            'description',
            sqlmodel.sql.sqltypes.AutoString(length=255),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_roles_name'),
        'roles',
        ['name'],
        unique=True,
    )

    op.create_table(
        'role_permission_links',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id']),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.PrimaryKeyConstraint('role_id', 'permission_id'),
    )

    op.create_table(
        'user_role_links',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('user_id', 'role_id'),
    )

    op.drop_column('users', 'role')


def downgrade() -> None:
    op.add_column(
        'users',
        sa.Column(
            'role',
            postgresql.ENUM(
                'STUDENT',
                'ADMIN',
                'MODERATOR',
                name='userrole',
                create_type=False,
            ),
            nullable=False,
            server_default='STUDENT',
        ),
    )

    op.drop_table('user_role_links')
    op.drop_table('role_permission_links')
    op.drop_index(op.f('ix_roles_name'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_permissions_scope'), table_name='permissions')
    op.drop_table('permissions')