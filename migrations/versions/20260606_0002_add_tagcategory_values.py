"""add tagcategory enum values

Revision ID: 20260606_0002
Revises: 20260606_0001
Create Date: 2026-06-06
"""

from typing import Sequence, Union

from alembic import op

revision: str = '20260606_0002'
down_revision: Union[str, None] = '20260606_0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TAG_CATEGORY_VALUES = [
    'sleep_schedule',
    'cleanliness',
    'noise_level',
    'guest_frequency',
    'smoking_preference',
    'alcohol_preference',
    'room_order_preference',
    'pet_preference',
    'interests',
]


def upgrade() -> None:
    for value in TAG_CATEGORY_VALUES:
        op.execute(
            f"ALTER TYPE tagcategory ADD VALUE IF NOT EXISTS '{value}'"
        )


def downgrade() -> None:
    pass