"""Add exploration and learning tables

Revision ID: add_exploration_learning
Revises: add_reminders_table
Create Date: 2026-01-28

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision = 'add_exploration_learning'
down_revision = 'add_reminders_table'
branch_labels = None
depends_on = None


def upgrade():
    # Exploration topics
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
    
    op.create_index('ix_exploration_topics_user_id', 'exploration_topics', ['user_id'])
    op.create_index('ix_exploration_topics_understanding', 'exploration_topics', ['understanding_score'])
    
    # Learned patterns
    op.create_table(
        'learned_patterns',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('pattern', sa.Text(), nullable=False),
        sa.Column('evidence', sa.Text(), nullable=True),
        sa.Column('confidence', sa.Integer(), default=50, nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    
    op.create_index('ix_learned_patterns_user_id', 'learned_patterns', ['user_id'])
    op.create_index('ix_learned_patterns_category', 'learned_patterns', ['category'])


def downgrade():
    op.drop_index('ix_learned_patterns_category')
    op.drop_index('ix_learned_patterns_user_id')
    op.drop_table('learned_patterns')
    
    op.drop_index('ix_exploration_topics_understanding')
    op.drop_index('ix_exploration_topics_user_id')
    op.drop_table('exploration_topics')
