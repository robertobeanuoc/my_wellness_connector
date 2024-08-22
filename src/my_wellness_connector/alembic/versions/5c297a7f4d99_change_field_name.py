"""change field name

Revision ID: 5c297a7f4d99
Revises: 92422a58d7ce
Create Date: 2024-08-22 10:22:07.582997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '5c297a7f4d99'
down_revision: Union[str, None] = '92422a58d7ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('session_exercise', sa.Column('machine_type_uuid', sa.String(length=100), nullable=True))
    op.create_foreign_key(None, 'session_exercise', 'machine_type', ['machine_type_uuid'], ['uuid'])
    op.drop_column('session_exercise', 'machine_type')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('session_exercise', sa.Column('machine_type', mysql.VARCHAR(length=100), nullable=True))
    op.drop_constraint(None, 'session_exercise', type_='foreignkey')
    op.drop_column('session_exercise', 'machine_type_uuid')
    # ### end Alembic commands ###