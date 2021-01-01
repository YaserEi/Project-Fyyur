"""empty message

Revision ID: 0d9bbb848436
Revises: 872e43483e85
Create Date: 2021-01-01 11:53:42.321721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d9bbb848436'
down_revision = '872e43483e85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'upcoming_shows')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('upcoming_shows', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
