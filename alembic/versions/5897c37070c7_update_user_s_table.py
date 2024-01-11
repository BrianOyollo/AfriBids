"""update user's table

Revision ID: 5897c37070c7
Revises: a04f70aac8cc
Create Date: 2024-01-11 08:09:33.420198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5897c37070c7'
down_revision: Union[str, None] = 'a04f70aac8cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
