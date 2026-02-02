"""Pattern tracking system - replaces simple learned_patterns with structured tracking

Revision ID: add_pattern_tracking
Revises: add_exploration_learning
Create Date: 2026-01-28

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


revision = 'add_pattern_tracking'
down_revision = 'add_exploration_learning'
branch_labels = None
depends_on = None


def upgrade():
    # Pattern categories - the 18 base categories + user-discovered ones
    op.create_table(
        'pattern_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('category_name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    
    op.create_index('ix_pattern_categories_user', 'pattern_categories', ['user_id'])
    op.create_index('ix_pattern_categories_name', 'pattern_categories', ['category_name'])
    
    # Pattern observations - individual data points
    op.create_table(
        'pattern_observations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('sub_pattern', sa.String(100), nullable=True),
        sa.Column('observation', sa.Text(), nullable=False),
        sa.Column('context', JSONB, default={}, nullable=False),
        sa.Column('observed_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['pattern_categories.id'], ondelete='CASCADE')
    )
    
    op.create_index('ix_pattern_observations_user', 'pattern_observations', ['user_id'])
    op.create_index('ix_pattern_observations_category', 'pattern_observations', ['category_id'])
    op.create_index('ix_pattern_observations_sub_pattern', 'pattern_observations', ['sub_pattern'])
    op.create_index('ix_pattern_observations_date', 'pattern_observations', ['observed_at'])
    
    # Pattern hypotheses - what Sandy thinks might be true
    op.create_table(
        'pattern_hypotheses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('sub_pattern', sa.String(100), nullable=True),
        sa.Column('hypothesis', sa.Text(), nullable=False),
        sa.Column('confidence', sa.Integer(), default=0, nullable=False),
        sa.Column('supporting_observations', sa.Integer(), default=0, nullable=False),
        sa.Column('contradicting_observations', sa.Integer(), default=0, nullable=False),
        sa.Column('last_updated', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('status', sa.String(20), default='exploring', nullable=False),
        sa.Column('needs_exploration', sa.Boolean(), default=False, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['pattern_categories.id'], ondelete='CASCADE')
    )
    
    op.create_index('ix_pattern_hypotheses_user', 'pattern_hypotheses', ['user_id'])
    op.create_index('ix_pattern_hypotheses_category', 'pattern_hypotheses', ['category_id'])
    op.create_index('ix_pattern_hypotheses_sub_pattern', 'pattern_hypotheses', ['sub_pattern'])
    op.create_index('ix_pattern_hypotheses_confidence', 'pattern_hypotheses', ['confidence'])
    op.create_index('ix_pattern_hypotheses_needs_exploration', 'pattern_hypotheses', ['needs_exploration'])


def downgrade():
    op.drop_index('ix_pattern_hypotheses_needs_exploration')
    op.drop_index('ix_pattern_hypotheses_confidence')
    op.drop_index('ix_pattern_hypotheses_sub_pattern')
    op.drop_index('ix_pattern_hypotheses_category')
    op.drop_index('ix_pattern_hypotheses_user')
    op.drop_table('pattern_hypotheses')
    
    op.drop_index('ix_pattern_observations_date')
    op.drop_index('ix_pattern_observations_sub_pattern')
    op.drop_index('ix_pattern_observations_category')
    op.drop_index('ix_pattern_observations_user')
    op.drop_table('pattern_observations')
    
    op.drop_index('ix_pattern_categories_name')
    op.drop_index('ix_pattern_categories_user')
    op.drop_table('pattern_categories')
