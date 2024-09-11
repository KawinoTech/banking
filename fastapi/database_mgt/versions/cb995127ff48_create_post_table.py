"""create post table

Revision ID: cb995127ff48
Revises: 
Create Date: 2024-04-05 12:27:36.199666

"""
from typing import Sequence, Union
from uuid import uuid4
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb995127ff48'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('idea', sa.Column('id', sa.String(100), primary_key=True, default=str(uuid4())),
                    sa.Column('title', sa.String(30), nullable=False),
                    sa.Column('brief_description', sa.String(100), nullable=False),
                    sa.Column('further_description', sa.Text, nullable=False),
                    sa.Column('date_posted', sa.DateTime, nullable=False, default=datetime.utcnow()),
                    sa.Column('is_implemented', sa.Boolean, default=False),
                    sa.Column('assigned_bonus', sa.Boolean, default=False))


def downgrade() -> None:
    op.drop_table('idea')