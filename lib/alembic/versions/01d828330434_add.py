"""Add

Revision ID: 01d828330434
Revises: 656df4be9fb8
Create Date: 2024-05-10 11:43:41.106603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01d828330434'
down_revision: Union[str, None] = '656df4be9fb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
