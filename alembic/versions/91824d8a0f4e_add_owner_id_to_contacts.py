"""Add owner_id to contacts

Revision ID: 91824d8a0f4e
Revises: e68633845ff2
Create Date: 2024-11-20 23:24:29.162757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91824d8a0f4e'
down_revision: Union[str, None] = 'e68633845ff2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'contacts', 'users', ['owner_id'], ['id'])
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.drop_constraint(None, 'contacts', type_='foreignkey')
    op.drop_column('contacts', 'owner_id')
    # ### end Alembic commands ###
