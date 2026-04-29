"""add message sent_at and is_read columns

Revision ID: 9a8c3d1b4f72
Revises: 7b5a0e2c4a19
Create Date: 2026-04-28 12:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9a8c3d1b4f72'
down_revision: Union[str, Sequence[str], None] = '7b5a0e2c4a19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'messages',
        sa.Column(
            'sent_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text('now()'),
        ),
    )
    op.add_column(
        'messages',
        sa.Column(
            'is_read',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('false'),
        ),
    )
    op.execute('UPDATE messages SET sent_at = created_at')
    op.execute('UPDATE messages SET is_read = opened_at IS NOT NULL')
    op.alter_column('messages', 'sent_at', server_default=None)
    op.alter_column('messages', 'is_read', server_default=None)


def downgrade() -> None:
    op.drop_column('messages', 'is_read')
    op.drop_column('messages', 'sent_at')
