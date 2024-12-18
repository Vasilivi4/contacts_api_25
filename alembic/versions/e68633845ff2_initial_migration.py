"""Initial migration

Revision ID: e68633845ff2
Revises: 1dcee45fd412
Create Date: 2024-11-20 21:08:04.655668

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e68633845ff2'
down_revision: Union[str, None] = '1dcee45fd412'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contacts', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('contacts', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('contacts', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=150),
               type_=sa.String(length=100),
               existing_nullable=False)
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=150),
               existing_nullable=False)
    op.drop_column('users', 'name')
    op.alter_column('contacts', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('contacts', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('contacts', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
