"""empty message

Revision ID: 65f93931622b
Revises: 90757fb6f0e0
Create Date: 2020-12-27 13:36:37.610281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65f93931622b'
down_revision = '90757fb6f0e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('past_show_count', sa.Integer(), nullable=True))
    op.add_column('Artist', sa.Column('past_shows', sa.String(length=120), nullable=True))
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.add_column('Artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('Artist', sa.Column('upcoing_shows_count', sa.Integer(), nullable=True))
    op.add_column('Artist', sa.Column('upcoming_shows', sa.String(length=120), nullable=True))
    op.add_column('Artist', sa.Column('website', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('past_show_count', sa.Integer(), nullable=True))
    op.add_column('Venue', sa.Column('past_shows', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('upcoing_shows_count', sa.Integer(), nullable=True))
    op.add_column('Venue', sa.Column('upcoming_shows', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('website', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'website')
    op.drop_column('Venue', 'upcoming_shows')
    op.drop_column('Venue', 'upcoing_shows_count')
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'past_shows')
    op.drop_column('Venue', 'past_show_count')
    op.drop_column('Venue', 'genres')
    op.drop_column('Artist', 'website')
    op.drop_column('Artist', 'upcoming_shows')
    op.drop_column('Artist', 'upcoing_shows_count')
    op.drop_column('Artist', 'seeking_venue')
    op.drop_column('Artist', 'seeking_description')
    op.drop_column('Artist', 'past_shows')
    op.drop_column('Artist', 'past_show_count')
    # ### end Alembic commands ###
