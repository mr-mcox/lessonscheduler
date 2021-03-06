"""Add teachers

Revision ID: 1748c08d2e7
Revises: 35ef8baea55
Create Date: 2015-11-02 19:41:01.678886

"""

# revision identifiers, used by Alembic.
revision = '1748c08d2e7'
down_revision = '35ef8baea55'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teacher',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teacher')
    ### end Alembic commands ###
