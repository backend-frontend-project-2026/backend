"""merge migration heads

Revision ID: 5db2b376c407
Revises: b79aa4a6e417, e8f4c2a1b6d9
Create Date: 2026-05-25 17:42:06.975567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel



# revision identifiers, used by Alembic.
revision: str = '5db2b376c407'
down_revision: Union[str, Sequence[str], None] = ('b79aa4a6e417', 'e8f4c2a1b6d9')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass