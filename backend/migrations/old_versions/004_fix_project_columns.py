"""fix project columns

Revision ID: fix_project_cols_004
Revises: fix_table_names_003
Create Date: 2026-02-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'fix_project_cols_004'
down_revision: Union[str, None] = 'fix_table_names_003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add missing columns to projects table that the model expects."""

    # Add deadline column
    op.add_column('projects',
        sa.Column('deadline', sa.DateTime(), nullable=True))

    # Add time tracking columns
    op.add_column('projects',
        sa.Column('estimated_hours', sa.Integer(), nullable=True))

    op.add_column('projects',
        sa.Column('actual_hours', sa.Integer(), nullable=True))

    # Add backburner columns
    op.add_column('projects',
        sa.Column('moved_to_backburner_at', sa.DateTime(), nullable=True))

    op.add_column('projects',
        sa.Column('backburner_reason', sa.Text(), nullable=True))


def downgrade() -> None:
    """Remove added columns."""
    op.drop_column('projects', 'backburner_reason')
    op.drop_column('projects', 'moved_to_backburner_at')
    op.drop_column('projects', 'actual_hours')
    op.drop_column('projects', 'estimated_hours')
    op.drop_column('projects', 'deadline')
