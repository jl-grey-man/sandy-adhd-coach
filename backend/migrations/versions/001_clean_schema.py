"""clean schema from current models

Revision ID: clean_schema_001
Revises:
Create Date: 2026-02-03

This migration creates the complete database schema matching all current models.
All 16 tables with correct column names and relationships.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'clean_schema_001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create ENUM types first
    op.execute("CREATE TYPE projectstatus AS ENUM ('active', 'backburner', 'done', 'archived')")
    op.execute("CREATE TYPE taskstatus AS ENUM ('todo', 'in_progress', 'done')")
    op.execute("CREATE TYPE taskpriority AS ENUM ('high', 'medium', 'low')")
    op.execute("CREATE TYPE taskenergylevel AS ENUM ('high', 'medium', 'low')")

    # 1. USERS table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('name', sa.String(100), nullable=True),
        sa.Column('timezone', sa.String(50), nullable=False, server_default='UTC'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('preferences', postgresql.JSONB, nullable=False, server_default='{"voice_enabled": true, "notification_enabled": true, "checkin_times": {"morning": "09:00", "evening": "20:00"}}'),
        sa.Column('adhd_profile', postgresql.JSONB, nullable=False, server_default='{}'),
        sa.Column('telegram_chat_id', sa.BigInteger(), nullable=True),
        sa.Column('telegram_username', sa.String(100), nullable=True),
        sa.Column('morning_briefing_time', sa.String(5), nullable=False, server_default='09:00'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_users_email', 'users', ['email'])

    # 2. CONVERSATIONS table (CORRECT SCHEMA)
    op.create_table('conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.String(100), nullable=True),
        sa.Column('user_message', sa.Text(), nullable=False),
        sa.Column('ai_response', sa.Text(), nullable=False),
        sa.Column('input_type', sa.String(20), nullable=False, server_default='text'),
        sa.Column('context', postgresql.JSONB, nullable=True),
        sa.Column('suggestions', postgresql.JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('idx_conversations_session_id', 'conversations', ['session_id'])
    op.create_index('idx_conversations_created_at', 'conversations', ['created_at'])

    # 3. GOALS table
    op.create_table('goals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('target_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('progress', sa.Integer(), nullable=True),
        sa.Column('extra_data', postgresql.JSONB, nullable=True),
        sa.CheckConstraint("category IN ('personal', 'work')", name='check_goal_category'),
        sa.CheckConstraint("status IN ('active', 'completed', 'paused', 'abandoned')", name='check_goal_status'),
        sa.CheckConstraint('progress >= 0 AND progress <= 100', name='check_goal_progress'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_goals_user_id', 'goals', ['user_id'])

    # 4. PROJECTS table (uses 'name' not 'title')
    op.create_table('projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', postgresql.ENUM('active', 'backburner', 'done', 'archived', name='projectstatus'), nullable=False, server_default='active'),
        sa.Column('deadline', sa.DateTime(), nullable=True),
        sa.Column('estimated_hours', sa.Integer(), nullable=True),
        sa.Column('actual_hours', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('moved_to_backburner_at', sa.DateTime(), nullable=True),
        sa.Column('backburner_reason', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_projects_user_status', 'projects', ['user_id', 'status'])
    op.create_index('idx_projects_deadline', 'projects', ['deadline'])

    # 5. TASKS table (has project_id, NOT goal_id)
    op.create_table('tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', postgresql.ENUM('todo', 'in_progress', 'done', name='taskstatus'), nullable=False, server_default='todo'),
        sa.Column('priority', postgresql.ENUM('high', 'medium', 'low', name='taskpriority'), nullable=True),
        sa.Column('energy_level', postgresql.ENUM('high', 'medium', 'low', name='taskenergylevel'), nullable=True),
        sa.Column('estimated_minutes', sa.Integer(), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_tasks_user_status', 'tasks', ['user_id', 'status'])
    op.create_index('idx_tasks_project', 'tasks', ['project_id'])
    op.create_index('idx_tasks_due_date', 'tasks', ['due_date'])

    # 6. MILESTONES table
    op.create_table('milestones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('check_in_date', sa.DateTime(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('user_response', sa.Text(), nullable=True),
        sa.Column('responded_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # 7. BACKBURNER_ITEMS table
    op.create_table('backburner_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('context_tags', postgresql.ARRAY(sa.String()), nullable=False, server_default='{}'),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('resurfaced_at', sa.DateTime(), nullable=True),
        sa.Column('activated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_backburner_user_id', 'backburner_items', ['user_id'])

    # 8. CALENDAR_EVENTS table
    op.create_table('calendar_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('external_id', sa.String(255), nullable=True),
        sa.Column('title', sa.String(200), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('location', sa.String(200), nullable=True),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('all_day', sa.Boolean(), nullable=True),
        sa.Column('calendar_source', sa.String(50), nullable=True),
        sa.Column('synced_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.UniqueConstraint('user_id', 'external_id', 'calendar_source', name='uq_user_calendar_event'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_calendar_user_id', 'calendar_events', ['user_id'])

    # 9. CHECKINS table
    op.create_table('checkins',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(20), nullable=False),
        sa.Column('overall_rating', sa.Integer(), nullable=True),
        sa.Column('energy_rating', sa.Integer(), nullable=True),
        sa.Column('focus_rating', sa.Integer(), nullable=True),
        sa.Column('mood_rating', sa.Integer(), nullable=True),
        sa.Column('stress_rating', sa.Integer(), nullable=True),
        sa.Column('responses', postgresql.JSONB, nullable=True),
        sa.Column('ai_analysis', sa.Text(), nullable=True),
        sa.Column('insights', postgresql.JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.CheckConstraint("type IN ('daily', 'weekly', 'monthly')", name='check_checkin_type'),
        sa.CheckConstraint('overall_rating >= 1 AND overall_rating <= 10', name='check_overall_rating'),
        sa.CheckConstraint('energy_rating >= 1 AND energy_rating <= 10', name='check_energy_rating'),
        sa.CheckConstraint('focus_rating >= 1 AND focus_rating <= 10', name='check_focus_rating'),
        sa.CheckConstraint('mood_rating >= 1 AND mood_rating <= 10', name='check_mood_rating'),
        sa.CheckConstraint('stress_rating >= 1 AND stress_rating <= 10', name='check_stress_rating'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_checkins_user_id', 'checkins', ['user_id'])

    # 10. METRICS table
    op.create_table('metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('metric_type', sa.String(50), nullable=False),
        sa.Column('value', postgresql.JSONB, nullable=False),
        sa.Column('recorded_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_metrics_user_id', 'metrics', ['user_id'])

    # 11. WORK_SESSIONS table
    op.create_table('work_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('energy_at_start', sa.Integer(), nullable=True),
        sa.Column('focus_at_start', sa.Integer(), nullable=True),
        sa.Column('strategy_used', sa.String(100), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=True),
        sa.Column('switched_task', sa.Boolean(), nullable=True),
        sa.Column('reason_for_switching', sa.Text(), nullable=True),
        sa.Column('effectiveness_rating', sa.Integer(), nullable=True),
        sa.CheckConstraint('energy_at_start >= 1 AND energy_at_start <= 10', name='check_session_energy'),
        sa.CheckConstraint('focus_at_start >= 1 AND focus_at_start <= 10', name='check_session_focus'),
        sa.CheckConstraint('effectiveness_rating >= 1 AND effectiveness_rating <= 10', name='check_session_effectiveness'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_work_sessions_user_id', 'work_sessions', ['user_id'])

    # 12. WHEEL_CATEGORIES table
    op.create_table('wheel_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('definition_of_10', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.UniqueConstraint('user_id', 'name', name='uq_user_wheel_category'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 13. WHEEL_SCORES table
    op.create_table('wheel_scores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('recorded_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.CheckConstraint('score >= 0 AND score <= 10', name='check_wheel_score'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['wheel_categories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 14. CONVERSATION_EMBEDDINGS table
    op.create_table('conversation_embeddings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('pinecone_id', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.UniqueConstraint('pinecone_id'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 15. PATTERN_CATEGORIES table
    op.create_table('pattern_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('category_name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('understanding_level', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('observations_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('current_hypothesis', sa.Text(), nullable=True),
        sa.Column('confidence', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('evidence', postgresql.JSONB, nullable=False, server_default='[]'),
        sa.Column('last_observed', sa.DateTime(), nullable=True),
        sa.Column('needs_exploration', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_pattern_categories_user_id', 'pattern_categories', ['user_id'])
    op.create_index('idx_pattern_categories_needs_exploration', 'pattern_categories', ['needs_exploration'])

    # 16. PATTERN_OBSERVATIONS table
    op.create_table('pattern_observations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('observation_type', sa.String(50), nullable=False),
        sa.Column('observation_text', sa.Text(), nullable=False),
        sa.Column('context', postgresql.JSONB, nullable=False, server_default='{}'),
        sa.Column('weight', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['pattern_categories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_pattern_observations_user_id', 'pattern_observations', ['user_id'])
    op.create_index('idx_pattern_observations_category_id', 'pattern_observations', ['category_id'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('pattern_observations')
    op.drop_table('pattern_categories')
    op.drop_table('conversation_embeddings')
    op.drop_table('wheel_scores')
    op.drop_table('wheel_categories')
    op.drop_table('work_sessions')
    op.drop_table('metrics')
    op.drop_table('checkins')
    op.drop_table('calendar_events')
    op.drop_table('backburner_items')
    op.drop_table('milestones')
    op.drop_table('tasks')
    op.drop_table('projects')
    op.drop_table('goals')
    op.drop_table('conversations')
    op.drop_table('users')

    # Drop ENUM types
    op.execute("DROP TYPE IF EXISTS taskenergylevel")
    op.execute("DROP TYPE IF EXISTS taskpriority")
    op.execute("DROP TYPE IF EXISTS taskstatus")
    op.execute("DROP TYPE IF EXISTS projectstatus")
