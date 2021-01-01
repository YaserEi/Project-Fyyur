"""empty message

Revision ID: 4914c7df9ae4
Revises: 91975529ea36
Create Date: 2020-12-31 13:49:10.044289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4914c7df9ae4'
down_revision = '91975529ea36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('upcoing_shows_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'upcoing_shows_count')
    # ### end Alembic commands ###
