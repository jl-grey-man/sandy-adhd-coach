"""Remove old exploration and learned_patterns tables

Revision ID: merge_to_pattern_system
Revises: add_pattern_tracking
Create Date: 2026-01-28

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


revision = 'merge_to_pattern_system'
down_revision = 'add_pattern_tracking'
branch_labels = None
depends_on = None


def upgrade():
    # Drop old tables - replaced by pattern_categories system
    op.execute('DROP TABLE IF EXISTS exploration_topics CASCADE')
    op.execute('DROP TABLE IF EXISTS learned_patterns CASCADE')


def downgrade():
    # Recreate old tables if needed
    op.create_table(
        'exploration_topics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('topic', sa.String(100), nullable=False),
        sa.Column('understanding_score', sa.Integer(), default=0, nullable=False),
        sa.Column('last_discussed', sa.DateTime(), nullable=True),
        sa.Column('priority', sa.Integer(), default=5, nullable=False),
        sa.Column('key_insights', JSONB, default={}, nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    
    op.create_table(
        'learned_patterns',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('pattern', sa.Text(), nullable=False),
        sa.Column('evidence', sa.Text(), nullable=True),
        sa.Column('confidence', sa.Integer(), default=50, nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
