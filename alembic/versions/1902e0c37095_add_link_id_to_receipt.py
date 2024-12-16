"""add_link_id_to_receipt

Revision ID: 1902e0c37095
Revises: 6fc1197c6a60
Create Date: 2024-12-16 23:01:15.440540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1902e0c37095'
down_revision: Union[str, None] = '6fc1197c6a60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('receipts', sa.Column('link_id', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'receipts', ['link_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'receipts', type_='unique')
    op.drop_column('receipts', 'link_id')
    # ### end Alembic commands ###
