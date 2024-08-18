"""add trace rows

Revision ID: 3a9c988b03d5
Revises: 5bac9ba21fac
Create Date: 2024-08-18 17:10:06.949992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a9c988b03d5'
down_revision: Union[str, None] = '5bac9ba21fac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercise_type', sa.Column('row_created_at', sa.DateTime(), nullable=False))
    op.add_column('exercise_type', sa.Column('row_updated_at', sa.DateTime(), nullable=True))
    op.add_column('machine_type', sa.Column('row_created_at', sa.DateTime(), nullable=False))
    op.add_column('machine_type', sa.Column('row_updated_at', sa.DateTime(), nullable=True))
    op.add_column('session_exercise', sa.Column('row_created_at', sa.DateTime(), nullable=False))
    op.add_column('session_exercise', sa.Column('row_updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('session_exercise', 'row_updated_at')
    op.drop_column('session_exercise', 'row_created_at')
    op.drop_column('machine_type', 'row_updated_at')
    op.drop_column('machine_type', 'row_created_at')
    op.drop_column('exercise_type', 'row_updated_at')
    op.drop_column('exercise_type', 'row_created_at')
    # ### end Alembic commands ###
