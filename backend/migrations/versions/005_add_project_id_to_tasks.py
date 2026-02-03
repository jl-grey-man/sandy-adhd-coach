"""add project_id to tasks

Revision ID: add_project_id_005
Revises: fix_project_cols_004
Create Date: 2026-02-03

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_project_id_005'
down_revision = 'fix_project_cols_004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add project_id column to tasks table
    op.add_column('tasks', sa.Column('project_id', sa.Integer(), nullable=True))

    # Add foreign key constraint
    op.create_foreign_key(
        'fk_tasks_project_id',
        'tasks', 'projects',
        ['project_id'], ['id']
    )

    # Create index for project_id
    op.create_index('idx_tasks_project', 'tasks', ['project_id'])


def downgrade() -> None:
    op.drop_index('idx_tasks_project', table_name='tasks')
    op.drop_constraint('fk_tasks_project_id', 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'project_id')
