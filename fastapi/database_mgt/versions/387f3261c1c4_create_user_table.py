"""create user table

Revision ID: 387f3261c1c4
Revises: cb995127ff48
Create Date: 2024-04-05 13:25:40.674619

"""
from typing import Sequence, Union
from uuid import uuid4
from datetime import datetime

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '387f3261c1c4'
down_revision: Union[str, None] = 'cb995127ff48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user', sa.Column('id', sa.String(100), primary_key=True, default=str(uuid4())),
                    sa.Column('username', sa.String(20), unique=True, nullable=False),
                    sa.Column('image_file', sa.String(20), nullable=True, default='default.jpg'),
                    sa.Column('password_hash', sa.String(60), nullable=False),
                    sa.Column('email', sa.String(60), nullable=False, unique=True),
                    sa.Column('score', sa.Integer, default=0),
                    sa.Column('department', sa.String(100))
                    )


def downgrade() -> None:
    op.drop_table('user')