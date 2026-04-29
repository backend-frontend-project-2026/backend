"""update complaint status enum

Revision ID: 7b5a0e2c4a19
Revises: 95f39cef3923
Create Date: 2026-04-24 20:00:00.000000

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7b5a0e2c4a19'
down_revision: Union[str, Sequence[str], None] = '95f39cef3923'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TYPE complaintstatus_new AS ENUM (
            'NEW',
            'IN_PROGRESS',
            'RESOLVED',
            'REJECTED'
        )
        """
    )
    op.execute(
        """
        ALTER TABLE complaints
        ALTER COLUMN status TYPE complaintstatus_new
        USING CASE
            WHEN status::text = 'CREATED' THEN 'NEW'
            ELSE status::text
        END::complaintstatus_new
        """
    )
    op.execute('DROP TYPE complaintstatus')
    op.execute('ALTER TYPE complaintstatus_new RENAME TO complaintstatus')


def downgrade() -> None:
    op.execute(
        """
        CREATE TYPE complaintstatus_old AS ENUM (
            'CREATED',
            'RESOLVED',
            'REJECTED'
        )
        """
    )
    op.execute(
        """
        ALTER TABLE complaints
        ALTER COLUMN status TYPE complaintstatus_old
        USING CASE
            WHEN status::text IN ('NEW', 'IN_PROGRESS') THEN 'CREATED'
            ELSE status::text
        END::complaintstatus_old
        """
    )
    op.execute('DROP TYPE complaintstatus')
    op.execute('ALTER TYPE complaintstatus_old RENAME TO complaintstatus')
