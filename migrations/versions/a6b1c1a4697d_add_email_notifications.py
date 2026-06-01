"""add email notifications

Revision ID: a6b1c1a4697d
Revises: 116692ea3208
Create Date: 2026-06-01 16:22:56.181411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a6b1c1a4697d'
down_revision: Union[str, Sequence[str], None] = '116692ea3208'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
            CREATE TYPE emailnotificationaction AS ENUM (
                'CONFIRM_ACCOUNT',
                'RESET_PASSWORD'
            );
        EXCEPTION
            WHEN duplicate_object THEN NULL;
        END $$;
        """
    )

    emailnotificationaction = postgresql.ENUM(
        'CONFIRM_ACCOUNT',
        'RESET_PASSWORD',
        name='emailnotificationaction',
        create_type=False,
    )

    op.create_table(
        'email_notifications',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column(
            'recipient_email',
            sqlmodel.sql.sqltypes.AutoString(length=255),
            nullable=False,
        ),
        sa.Column(
            'action',
            emailnotificationaction,
            nullable=False,
        ),
        sa.Column(
            'code',
            sqlmodel.sql.sqltypes.AutoString(length=64),
            nullable=False,
        ),
        sa.Column('is_used', sa.Boolean(), nullable=False),
        sa.Column('expires_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('used_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_index(
        op.f('ix_email_notifications_user_id'),
        'email_notifications',
        ['user_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_email_notifications_recipient_email'),
        'email_notifications',
        ['recipient_email'],
        unique=False,
    )
    op.create_index(
        op.f('ix_email_notifications_action'),
        'email_notifications',
        ['action'],
        unique=False,
    )
    op.create_index(
        op.f('ix_email_notifications_code'),
        'email_notifications',
        ['code'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f('ix_email_notifications_code'),
        table_name='email_notifications',
    )
    op.drop_index(
        op.f('ix_email_notifications_action'),
        table_name='email_notifications',
    )
    op.drop_index(
        op.f('ix_email_notifications_recipient_email'),
        table_name='email_notifications',
    )
    op.drop_index(
        op.f('ix_email_notifications_user_id'),
        table_name='email_notifications',
    )
    op.drop_table('email_notifications')

    op.execute('DROP TYPE IF EXISTS emailnotificationaction')