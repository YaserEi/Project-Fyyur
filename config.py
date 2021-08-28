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


SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/Fyyur'
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)
if not database_exists(engine.url):
    create_database(engine.url)
SQLALCHEMY_TRACK_MODIFICATIONS =False
