"""add all missing tables

Revision ID: add_all_missing_tables
Revises: add_missing_user_cols
Create Date: 2026-02-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_all_missing_tables'
down_revision: Union[str, None] = 'add_missing_user_cols'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add all missing tables that exist in models but not in migrations."""

    # 1. Goals table
    op.create_table('goals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('target_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='active'),
        sa.Column('progress', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('extra_data', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.CheckConstraint("category IN ('personal', 'work')", name='check_goal_category'),
        sa.CheckConstraint("status IN ('active', 'completed', 'paused', 'abandoned')", name='check_goal_status'),
        sa.CheckConstraint("progress >= 0 AND progress <= 100", name='check_goal_progress'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_goals_user_id', 'goals', ['user_id'])

    # 2. Checkins table
    op.create_table('checkins',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=20), nullable=False),
        sa.Column('overall_rating', sa.Integer(), nullable=True),
        sa.Column('energy_rating', sa.Integer(), nullable=True),
        sa.Column('focus_rating', sa.Integer(), nullable=True),
        sa.Column('mood_rating', sa.Integer(), nullable=True),
        sa.Column('stress_rating', sa.Integer(), nullable=True),
        sa.Column('responses', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('ai_analysis', sa.Text(), nullable=True),
        sa.Column('insights', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint("type IN ('daily', 'weekly', 'monthly')", name='check_checkin_type'),
        sa.CheckConstraint("overall_rating >= 1 AND overall_rating <= 10", name='check_overall_rating'),
        sa.CheckConstraint("energy_rating >= 1 AND energy_rating <= 10", name='check_energy_rating'),
        sa.CheckConstraint("focus_rating >= 1 AND focus_rating <= 10", name='check_focus_rating'),
        sa.CheckConstraint("mood_rating >= 1 AND mood_rating <= 10", name='check_mood_rating'),
        sa.CheckConstraint("stress_rating >= 1 AND stress_rating <= 10", name='check_stress_rating'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_checkins_user_id', 'checkins', ['user_id'])

    # 3. Conversation Embeddings table
    op.create_table('conversation_embeddings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('pinecone_id', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('pinecone_id')
    )

    # 4. Fix calendar table name (drop old, create new)
    op.drop_table('calendar')
    op.create_table('calendar_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('external_id', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('location', sa.String(length=200), nullable=True),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('all_day', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('calendar_source', sa.String(length=50), nullable=False, server_default='google'),
        sa.Column('synced_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'external_id', 'calendar_source', name='uq_user_calendar_event')
    )
    op.create_index('ix_calendar_events_user_id', 'calendar_events', ['user_id'])

    # 5. Fix backburner table name (drop old, create new)
    op.drop_table('backburner')
    op.create_table('backburner_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('context_tags', postgresql.ARRAY(sa.String()), nullable=False, server_default='{}'),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('resurfaced_at', sa.DateTime(), nullable=True),
        sa.Column('activated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_backburner_user', 'backburner_items', ['user_id'])

    # 6. Fix wheel table (drop old, create two new tables)
    op.drop_table('wheel')

    op.create_table('wheel_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('definition_of_10', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'name', name='uq_user_wheel_category')
    )

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

    # 7. Fix work_sessions table (drop old, create with correct columns)
    op.drop_table('work_sessions')
    op.create_table('work_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('energy_at_start', sa.Integer(), nullable=True),
        sa.Column('focus_at_start', sa.Integer(), nullable=True),
        sa.Column('strategy_used', sa.String(length=100), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('switched_task', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('reason_for_switching', sa.Text(), nullable=True),
        sa.Column('effectiveness_rating', sa.Integer(), nullable=True),
        sa.CheckConstraint("energy_at_start >= 1 AND energy_at_start <= 10", name='check_session_energy'),
        sa.CheckConstraint("focus_at_start >= 1 AND focus_at_start <= 10", name='check_session_focus'),
        sa.CheckConstraint("effectiveness_rating >= 1 AND effectiveness_rating <= 10", name='check_session_effectiveness'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_work_sessions_user_id', 'work_sessions', ['user_id'])
    op.create_index('ix_work_sessions_task_id', 'work_sessions', ['task_id'])


def downgrade() -> None:
    """Drop all added/fixed tables."""
    op.drop_table('work_sessions')
    op.drop_table('wheel_scores')
    op.drop_table('wheel_categories')
    op.drop_table('backburner_items')
    op.drop_table('calendar_events')
    op.drop_table('conversation_embeddings')
    op.drop_table('checkins')
    op.drop_table('goals')
