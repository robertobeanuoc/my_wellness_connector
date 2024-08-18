"""add machine type

Revision ID: b2bda73e7bcf
Revises: 211af0b464fe
Create Date: 2024-08-18 16:51:19.364987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2bda73e7bcf'
down_revision: Union[str, None] = '211af0b464fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('machine_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('machine_type')
    # ### end Alembic commands ###
