"""align schema with current models

Revision ID: e8f4c2a1b6d9
Revises: c1f0b3d84a2e
Create Date: 2026-04-28 19:20:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e8f4c2a1b6d9'
down_revision: Union[str, Sequence[str], None] = 'c1f0b3d84a2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DEAL_TITLE_MAX_LENGTH = 120
MESSAGE_CONTENT_MAX_LENGTH = 1000


def _get_columns(table_name: str) -> dict[str, dict[str, object]]:
    inspector = sa.inspect(op.get_bind())
    return {
        column['name']: column for column in inspector.get_columns(table_name)
    }


def _find_foreign_key_name(
    table_name: str,
    constrained_columns: list[str],
    referred_table: str,
) -> str | None:
    inspector = sa.inspect(op.get_bind())
    for foreign_key in inspector.get_foreign_keys(table_name):
        if (
            foreign_key.get('constrained_columns') == constrained_columns
            and foreign_key.get('referred_table') == referred_table
        ):
            return foreign_key.get('name')
    return None


def _ensure_dorm_city() -> None:
    columns = _get_columns('dorms')
    if 'city' not in columns:
        op.add_column(
            'dorms',
            sa.Column(
                'city',
                sa.String(),
                nullable=False,
                server_default=sa.text("''"),
            ),
        )
        op.execute(
            """
            UPDATE dorms
            SET city = COALESCE(universities.city, '')
            FROM universities
            WHERE dorms.uni_id = universities.id
            """
        )
        op.alter_column('dorms', 'city', server_default=None)
        return

    if bool(columns['city']['nullable']):
        op.execute(
            """
            UPDATE dorms
            SET city = COALESCE(city, universities.city, '')
            FROM universities
            WHERE dorms.uni_id = universities.id
            """
        )
        op.execute("UPDATE dorms SET city = '' WHERE city IS NULL")
        op.alter_column('dorms', 'city', nullable=False)


def _ensure_profiles_faculty() -> None:
    columns = _get_columns('profiles')
    if 'faculty_id' not in columns:
        op.add_column('profiles', sa.Column('faculty_id', sa.Integer(), nullable=True))

    foreign_key_name = _find_foreign_key_name(
        'profiles', ['faculty_id'], 'faculties'
    )
    if foreign_key_name is None:
        op.create_foreign_key(
            'fk_profiles_faculty_id_faculties',
            'profiles',
            'faculties',
            ['faculty_id'],
            ['id'],
        )

    op.execute(
        """
        UPDATE profiles
        SET faculty_id = candidate.faculty_id
        FROM (
            SELECT uni_id, MIN(id) AS faculty_id
            FROM faculties
            GROUP BY uni_id
            HAVING COUNT(*) = 1
        ) AS candidate
        WHERE profiles.uni_id = candidate.uni_id
          AND profiles.faculty_id IS NULL
        """
    )

    null_profiles = op.get_bind().execute(
        sa.text('SELECT COUNT(*) FROM profiles WHERE faculty_id IS NULL')
    ).scalar_one()
    if null_profiles:
        raise RuntimeError(
            'Cannot upgrade profiles.faculty_id automatically: '
            'manual backfill is required for existing profiles.'
        )

    op.alter_column(
        'profiles',
        'faculty_id',
        existing_type=sa.Integer(),
        nullable=False,
    )

    if 'profile_picture_url' in columns:
        op.drop_column('profiles', 'profile_picture_url')


def _sync_deals_shape() -> None:
    columns = _get_columns('deals')
    if 'status' in columns:
        op.drop_column('deals', 'status')
    op.execute('DROP TYPE IF EXISTS dealstatus')

    title_type = columns['title']['type']
    if getattr(title_type, 'length', None) != DEAL_TITLE_MAX_LENGTH:
        op.alter_column(
            'deals',
            'title',
            type_=sa.String(length=DEAL_TITLE_MAX_LENGTH),
            existing_type=title_type,
        )


def _sync_messages_shape() -> None:
    columns = _get_columns('messages')
    if 'opened_at' in columns:
        op.drop_column('messages', 'opened_at')

    content_type = columns['content']['type']
    if getattr(content_type, 'length', None) != MESSAGE_CONTENT_MAX_LENGTH:
        op.alter_column(
            'messages',
            'content',
            type_=sa.String(length=MESSAGE_CONTENT_MAX_LENGTH),
            existing_type=content_type,
        )


def _sync_complaints_attachment_column() -> None:
    columns = _get_columns('complaints')
    if (
        'screenshots' in columns
        and 'screenshot_url_for_report' not in columns
    ):
        op.alter_column(
            'complaints',
            'screenshots',
            new_column_name='screenshot_url_for_report',
            existing_type=columns['screenshots']['type'],
            existing_nullable=bool(columns['screenshots']['nullable']),
        )
        return

    if 'screenshots' in columns and 'screenshot_url_for_report' in columns:
        op.execute(
            """
            UPDATE complaints
            SET screenshot_url_for_report = COALESCE(
                screenshot_url_for_report,
                screenshots
            )
            """
        )
        op.drop_column('complaints', 'screenshots')


def upgrade() -> None:
    _sync_complaints_attachment_column()
    _ensure_dorm_city()
    _ensure_profiles_faculty()
    _sync_deals_shape()
    _sync_messages_shape()


def downgrade() -> None:
    complaints_columns = _get_columns('complaints')
    if (
        'screenshot_url_for_report' in complaints_columns
        and 'screenshots' not in complaints_columns
    ):
        op.alter_column(
            'complaints',
            'screenshot_url_for_report',
            new_column_name='screenshots',
            existing_type=complaints_columns['screenshot_url_for_report']['type'],
            existing_nullable=bool(
                complaints_columns['screenshot_url_for_report']['nullable']
            ),
        )

    message_columns = _get_columns('messages')
    if 'opened_at' not in message_columns:
        op.add_column(
            'messages',
            sa.Column('opened_at', sa.DateTime(timezone=True), nullable=True),
        )
    op.alter_column(
        'messages',
        'content',
        type_=sa.String(),
        existing_type=message_columns['content']['type'],
    )

    deal_columns = _get_columns('deals')
    if 'status' not in deal_columns:
        op.execute(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1
                    FROM pg_type
                    WHERE typname = 'dealstatus'
                ) THEN
                    CREATE TYPE dealstatus AS ENUM (
                        'ACTIVE',
                        'CLOSED',
                        'CANCELLED'
                    );
                END IF;
            END $$;
            """
        )
        op.add_column(
            'deals',
            sa.Column(
                'status',
                sa.Enum('ACTIVE', 'CLOSED', 'CANCELLED', name='dealstatus'),
                nullable=False,
                server_default=sa.text("'ACTIVE'"),
            ),
        )
        op.alter_column('deals', 'status', server_default=None)
    op.alter_column(
        'deals',
        'title',
        type_=sa.String(length=100),
        existing_type=deal_columns['title']['type'],
    )

    profile_columns = _get_columns('profiles')
    if 'profile_picture_url' not in profile_columns:
        op.add_column(
            'profiles',
            sa.Column('profile_picture_url', sa.String(), nullable=True),
        )
    foreign_key_name = _find_foreign_key_name(
        'profiles', ['faculty_id'], 'faculties'
    )
    if foreign_key_name is not None:
        op.drop_constraint(foreign_key_name, 'profiles', type_='foreignkey')
    if 'faculty_id' in profile_columns:
        op.drop_column('profiles', 'faculty_id')

    dorm_columns = _get_columns('dorms')
    if 'city' in dorm_columns:
        op.drop_column('dorms', 'city')
