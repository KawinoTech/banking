"""Create Foreign Key to Idea Table

Revision ID: 5602f683606a
Revises: 387f3261c1c4
Create Date: 2024-04-05 14:28:25.389983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5602f683606a'
down_revision: Union[str, None] = '387f3261c1c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('idea', sa.Column('user_id', sa.String(100), nullable=False))
    op.create_foreign_key('userfk', source_table='idea', referent_table='user', local_cols=['user_id'],
                          remote_cols=['id'], ondelete=['CASACADE'])


def downgrade() -> None:
    op.drop_constraint('userfk', table_name='idea')
    op.drop_column('idea', 'user_id')
