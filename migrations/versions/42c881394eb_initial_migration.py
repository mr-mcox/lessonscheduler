"""initial migration

Revision ID: 42c881394eb
Revises: None
Create Date: 2015-10-27 19:50:06.577412

"""

# revision identifiers, used by Alembic.
revision = '42c881394eb'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('students')
    ### end Alembic commands ###