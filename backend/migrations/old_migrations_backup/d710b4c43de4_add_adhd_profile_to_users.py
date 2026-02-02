"""add adhd_profile to users

Revision ID: d710b4c43de4
Revises: 7f6c46148b8a
Create Date: 2026-01-27 10:19:34.320587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd710b4c43de4'
down_revision: Union[str, Sequence[str], None] = '7f6c46148b8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('adhd_profile', sa.dialects.postgresql.JSONB(), nullable=True, server_default='{}'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'adhd_profile')
