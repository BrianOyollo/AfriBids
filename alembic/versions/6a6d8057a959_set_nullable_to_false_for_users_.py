"""set nullable to false for users.username and users.email

Revision ID: 6a6d8057a959
Revises: 5897c37070c7
Create Date: 2024-01-11 09:42:15.468652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a6d8057a959'
down_revision: Union[str, None] = '5897c37070c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
