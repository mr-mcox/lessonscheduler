"""Add schedule day

Revision ID: 1656bc5bfbe
Revises: 1748c08d2e7
Create Date: 2015-11-02 19:49:54.647524

"""

# revision identifiers, used by Alembic.
revision = '1656bc5bfbe'
down_revision = '1748c08d2e7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('schedule_days',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('schedule_days')
    ### end Alembic commands ###