"""fix conversations schema

Revision ID: fix_conversations_006
Revises: add_project_id_005
Create Date: 2026-02-03

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fix_conversations_006'
down_revision = 'add_project_id_005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop old columns
    op.drop_column('conversations', 'role')
    op.drop_column('conversations', 'content')

    # Add new columns
    op.add_column('conversations', sa.Column('user_message', sa.Text(), nullable=False, server_default=''))
    op.add_column('conversations', sa.Column('ai_response', sa.Text(), nullable=False, server_default=''))
    op.add_column('conversations', sa.Column('input_type', sa.String(20), nullable=False, server_default='text'))
    op.add_column('conversations', sa.Column('context', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('conversations', sa.Column('suggestions', postgresql.JSONB(astext_type=sa.Text()), nullable=True))

    # Make session_id nullable
    op.alter_column('conversations', 'session_id', nullable=True)

    # Add missing index
    op.create_index('idx_conversations_created_at', 'conversations', ['created_at'])


def downgrade() -> None:
    op.drop_index('idx_conversations_created_at', table_name='conversations')
    op.alter_column('conversations', 'session_id', nullable=False)
    op.drop_column('conversations', 'suggestions')
    op.drop_column('conversations', 'context')
    op.drop_column('conversations', 'input_type')
    op.drop_column('conversations', 'ai_response')
    op.drop_column('conversations', 'user_message')
    op.add_column('conversations', sa.Column('content', sa.Text(), nullable=False))
    op.add_column('conversations', sa.Column('role', sa.String(20), nullable=False))
