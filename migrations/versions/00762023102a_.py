"""empty message

Revision ID: 00762023102a
Revises: 04bcbafdbea3
Create Date: 2020-04-30 15:33:25.840847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00762023102a'
down_revision = '04bcbafdbea3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
