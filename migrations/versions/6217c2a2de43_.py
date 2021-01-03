"""empty message

Revision ID: 6217c2a2de43
Revises: 17c6c0d5377d
Create Date: 2021-01-03 13:05:30.567246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6217c2a2de43'
down_revision = '17c6c0d5377d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'upcoming_shows')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('upcoming_shows', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
