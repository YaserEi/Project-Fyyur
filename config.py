import os
import flask
from flask_migrate import Migrate
import sqlalchemy
from sqlalchemy_utils import database_exists, create_database
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


SQLALCHEMY_DATABASE_URI = 'postgres://vjswdqptfywcof:f4735bab158723cceb7e9a1be25a78817176c70a40e3485c34e028056674593e@ec2-54-147-126-173.compute-1.amazonaws.com:5432/dfte2k4o7nehqb'

engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)
if not database_exists(engine.url):
    create_database(engine.url)
SQLALCHEMY_TRACK_MODIFICATIONS =False
