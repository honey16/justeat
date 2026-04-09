"""add restaurant email

Revision ID: 4dccb39c4408
Revises: 
Create Date: 2026-04-08 11:10:29.079382

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4dccb39c4408'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('restaurants', sa.Column('email', sa.String(100)))


def downgrade() -> None:
    op.drop_column('restaurants', 'email')
