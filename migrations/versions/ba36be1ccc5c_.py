"""empty message

Revision ID: ba36be1ccc5c
Revises: 865403aeaf12
Create Date: 2022-06-26 19:25:00.325543

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ba36be1ccc5c'
down_revision = '865403aeaf12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('authors', 'date_of_death',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('authors', 'biography',
               existing_type=sa.TEXT(),
               nullable=True)
    op.add_column('books', sa.Column('quantity', sa.Integer(), nullable=False))
    op.add_column('rentals', sa.Column('quantity', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rentals', 'quantity')
    op.drop_column('books', 'quantity')
    op.alter_column('authors', 'biography',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('authors', 'date_of_death',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###
