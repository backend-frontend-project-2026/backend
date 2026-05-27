"""add refresh sessions

Revision ID: dee830e54421
Revises: 5db2b376c407
Create Date: 2026-05-25 17:52:21.188296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'dee830e54421'
down_revision: Union[str, Sequence[str], None] = (
    'b79aa4a6e417',
    'e8f4c2a1b6d9',
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'refresh_sessions',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column(
            'access_token_jti',
            sqlmodel.sql.sqltypes.AutoString(length=255),
            nullable=False,
        ),
        sa.Column(
            'refresh_token_jti',
            sqlmodel.sql.sqltypes.AutoString(length=255),
            nullable=False,
        ),
        sa.Column('expires_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('invalidated_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('is_invalidated', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_refresh_sessions_access_token_jti'),
        'refresh_sessions',
        ['access_token_jti'],
        unique=True,
    )
    op.create_index(
        op.f('ix_refresh_sessions_refresh_token_jti'),
        'refresh_sessions',
        ['refresh_token_jti'],
        unique=True,
    )
    op.create_index(
        op.f('ix_refresh_sessions_user_id'),
        'refresh_sessions',
        ['user_id'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f('ix_refresh_sessions_user_id'),
        table_name='refresh_sessions',
    )
    op.drop_index(
        op.f('ix_refresh_sessions_refresh_token_jti'),
        table_name='refresh_sessions',
    )
    op.drop_index(
        op.f('ix_refresh_sessions_access_token_jti'),
        table_name='refresh_sessions',
    )
    op.drop_table('refresh_sessions')