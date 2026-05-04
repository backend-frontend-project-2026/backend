"""sync models with current api

Revision ID: c1f0b3d84a2e
Revises: 9a8c3d1b4f72
Create Date: 2026-04-28 12:30:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c1f0b3d84a2e'
down_revision: Union[str, Sequence[str], None] = '9a8c3d1b4f72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TYPE userrole_new AS ENUM (
            'USER',
            'ADMIN'
        )
        """
    )
    op.execute(
        """
        ALTER TABLE users
        ALTER COLUMN role TYPE userrole_new
        USING CASE
            WHEN role::text IN ('STUDENT', 'MODERATOR') THEN 'USER'
            ELSE 'ADMIN'
        END::userrole_new
        """
    )
    op.execute('DROP TYPE userrole')
    op.execute('ALTER TYPE userrole_new RENAME TO userrole')

    op.add_column(
        'universities',
        sa.Column(
            'city',
            sa.String(),
            nullable=False,
            server_default=sa.text("''"),
        ),
    )
    op.execute("UPDATE universities SET city = '' WHERE city IS NULL")
    op.alter_column('universities', 'city', server_default=None)

    op.add_column(
        'profiles',
        sa.Column('profile_description', sa.String(), nullable=True),
    )
    op.add_column('profiles', sa.Column('course', sa.Integer(), nullable=True))
    op.add_column(
        'profiles',
        sa.Column(
            'city',
            sa.String(),
            nullable=False,
            server_default=sa.text("''"),
        ),
    )
    op.execute(
        """
        UPDATE profiles
        SET city = COALESCE(neighbourhoods.city, '')
        FROM neighbourhoods
        WHERE profiles.neighbourhood_id = neighbourhoods.id
        """
    )
    op.alter_column('profiles', 'city', server_default=None)
    op.alter_column('profiles', 'neighbourhood_id', nullable=True)

    op.add_column(
        'deals',
        sa.Column(
            'city',
            sa.String(),
            nullable=False,
            server_default=sa.text("''"),
        ),
    )
    op.execute(
        """
        UPDATE deals
        SET city = COALESCE(neighbourhoods.city, '')
        FROM neighbourhoods
        WHERE deals.neighbourhood_id = neighbourhoods.id
        """
    )
    op.alter_column('deals', 'city', server_default=None)
    op.alter_column('deals', 'budget_min', nullable=True)
    op.alter_column('deals', 'neighbourhood_id', nullable=True)


def downgrade() -> None:
    op.alter_column('deals', 'neighbourhood_id', nullable=False)
    op.alter_column('deals', 'budget_min', nullable=False)
    op.drop_column('deals', 'city')

    op.alter_column('profiles', 'neighbourhood_id', nullable=False)
    op.drop_column('profiles', 'city')
    op.drop_column('profiles', 'course')
    op.drop_column('profiles', 'profile_description')

    op.drop_column('universities', 'city')

    op.execute(
        """
        CREATE TYPE userrole_old AS ENUM (
            'STUDENT',
            'ADMIN',
            'MODERATOR'
        )
        """
    )
    op.execute(
        """
        ALTER TABLE users
        ALTER COLUMN role TYPE userrole_old
        USING CASE
            WHEN role::text = 'USER' THEN 'STUDENT'
            ELSE 'ADMIN'
        END::userrole_old
        """
    )
    op.execute('DROP TYPE userrole')
    op.execute('ALTER TYPE userrole_old RENAME TO userrole')
