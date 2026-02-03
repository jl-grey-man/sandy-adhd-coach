"""add missing user columns

Revision ID: add_missing_user_cols
Revises: initial_schema_001
Create Date: 2026-02-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_missing_user_cols'
down_revision: Union[str, None] = 'initial_schema_001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add missing columns to users table."""

    # Add preferences column
    op.add_column('users',
        sa.Column('preferences', postgresql.JSONB(astext_type=sa.Text()),
                  nullable=False,
                  server_default='{"voice_enabled": true, "notification_enabled": true, "checkin_times": {"morning": "09:00", "evening": "20:00"}}')
    )

    # Add adhd_profile column
    op.add_column('users',
        sa.Column('adhd_profile', postgresql.JSONB(astext_type=sa.Text()),
                  nullable=False,
                  server_default='{}')
    )

    # Add morning_briefing_time column
    op.add_column('users',
        sa.Column('morning_briefing_time', sa.String(length=5),
                  nullable=False,
                  server_default='09:00')
    )


def downgrade() -> None:
    """Remove added columns."""
    op.drop_column('users', 'morning_briefing_time')
    op.drop_column('users', 'adhd_profile')
    op.drop_column('users', 'preferences')
