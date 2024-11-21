"""add hashed_password column to users

Revision ID: 1dcee45fd412
Revises: 
Create Date: 2024-11-19 21:11:22.034634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1dcee45fd412'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_notes_id', table_name='notes')
    op.drop_table('notes')
    op.drop_index('ix_contacts_phone_number', table_name='contacts')
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=True))
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.drop_column('users', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    op.drop_column('users', 'hashed_password')
    op.create_index('ix_contacts_phone_number', 'contacts', ['phone_number'], unique=True)
    op.create_table('notes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('done', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='notes_pkey')
    )
    op.create_index('ix_notes_id', 'notes', ['id'], unique=False)
    # ### end Alembic commands ###