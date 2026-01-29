"""Create reminders table

Revision ID: add_reminders_table
Revises: 
Create Date: 2026-01-28

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_reminders_table'
down_revision = '3d8c242a2745'  # Link to the project management tables migration
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'reminders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('remind_at', sa.DateTime(), nullable=False),
        sa.Column('sent', sa.Boolean(), default=False, nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    
    op.create_index('ix_reminders_user_id', 'reminders', ['user_id'])
    op.create_index('ix_reminders_remind_at', 'reminders', ['remind_at'])
    op.create_index('ix_reminders_sent', 'reminders', ['sent'])


def downgrade():
    op.drop_index('ix_reminders_sent')
    op.drop_index('ix_reminders_remind_at')
    op.drop_index('ix_reminders_user_id')
    op.drop_table('reminders')
