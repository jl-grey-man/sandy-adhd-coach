"""add session_id to conversations

Revision ID: 42f417f227b3
Revises: d710b4c43de4
Create Date: 2026-01-27 10:39:14.560723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42f417f227b3'
down_revision: Union[str, Sequence[str], None] = 'd710b4c43de4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('conversations', sa.Column('session_id', sa.String(100), nullable=True))
    op.create_index('idx_conversations_session', 'conversations', ['session_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_conversations_session')
    op.drop_column('conversations', 'session_id')
