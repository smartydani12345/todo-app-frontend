"""Add language column to conversations table

Revision ID: add_language
Revises: 49bb83a0d2e3
Create Date: 2026-02-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'add_language'
down_revision: Union[str, Sequence[str], None] = '49bb83a0d2e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add language column to conversations table."""
    op.add_column('conversations', sa.Column('language', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False, server_default='en'))


def downgrade() -> None:
    """Remove language column from conversations table."""
    op.drop_column('conversations', 'language')
