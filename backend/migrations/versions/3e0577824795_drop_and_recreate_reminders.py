"""drop_and_recreate_reminders

Revision ID: 3e0577824795
Revises: 3b066e50a3e4
Create Date: 2026-01-31 08:54:53.901803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e0577824795'
down_revision: Union[str, Sequence[str], None] = '3b066e50a3e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Drop and recreate reminders table with correct schema."""
    # Drop the old table completely
    op.drop_table('reminders')
    
    # Create fresh table with correct schema
    op.create_table(
        'reminders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('task', sa.Text(), nullable=False),
        sa.Column('context', sa.Text(), nullable=True),
        sa.Column('reminder_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_sent', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_reminders_id'), 'reminders', ['id'], unique=False)
    op.create_index(op.f('ix_reminders_is_sent'), 'reminders', ['is_sent'], unique=False)
    op.create_index(op.f('ix_reminders_reminder_time'), 'reminders', ['reminder_time'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_reminders_reminder_time'), table_name='reminders')
    op.drop_index(op.f('ix_reminders_is_sent'), table_name='reminders')
    op.drop_index(op.f('ix_reminders_id'), table_name='reminders')
    op.drop_table('reminders')
