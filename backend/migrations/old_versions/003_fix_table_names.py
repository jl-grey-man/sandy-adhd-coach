"""fix table names

Revision ID: fix_table_names_003
Revises: add_missing_user_cols
Create Date: 2026-02-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fix_table_names_003'
down_revision: Union[str, None] = 'add_missing_user_cols'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename incorrectly named tables to match model definitions.

    Migration 001 created all tables but with wrong names:
    - calendar → calendar_events
    - backburner → backburner_items
    - wheel → need to split into wheel_categories + wheel_scores

    Also add conversation_embeddings table that was missing.
    """

    # 1. Rename calendar → calendar_events
    op.rename_table('calendar', 'calendar_events')

    # 2. Rename backburner → backburner_items
    op.rename_table('backburner', 'backburner_items')

    # 3. Rename indexes to match new table names
    op.execute('ALTER INDEX ix_calendar_user_id RENAME TO ix_calendar_events_user_id')
    op.execute('ALTER INDEX ix_calendar_start_time RENAME TO ix_calendar_events_start_time')
    op.execute('ALTER INDEX ix_backburner_user_id RENAME TO idx_backburner_user')

    # 4. Handle wheel table - rename to wheel_categories
    op.rename_table('wheel', 'wheel_categories')
    op.execute('ALTER INDEX ix_wheel_user_id RENAME TO ix_wheel_categories_user_id')

    # 5. Create wheel_scores table (split from wheel)
    op.create_table('wheel_scores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('recorded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['wheel_categories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 6. Add conversation_embeddings table (was completely missing)
    op.create_table('conversation_embeddings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('pinecone_id', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('pinecone_id')
    )


def downgrade() -> None:
    """Revert table renames."""
    op.drop_table('conversation_embeddings')
    op.drop_table('wheel_scores')
    op.rename_table('wheel_categories', 'wheel')
    op.rename_table('backburner_items', 'backburner')
    op.rename_table('calendar_events', 'calendar')
