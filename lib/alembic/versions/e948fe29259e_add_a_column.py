"""Add a column

Revision ID: e948fe29259e
Revises: 67471569b215
Create Date: 2024-05-10 15:20:55.696300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e948fe29259e'
down_revision: Union[str, None] = '67471569b215'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
