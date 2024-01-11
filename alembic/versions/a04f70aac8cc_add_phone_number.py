"""add phone number

Revision ID: a04f70aac8cc
Revises: 97063dbb8649
Create Date: 2024-01-11 07:26:37.307797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a04f70aac8cc'
down_revision: Union[str, None] = '97063dbb8649'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
