from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import db






class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent= db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    past_shows=db.Column(db.String(120))
    past_show_count= db.Column(db.Integer, default=0)
    upcoming_shows=db.Column(db.String(120), default="None")
    upcoming_shows_count=db.Column(db.Integer, default=0)
    genres = db.relationship('Genres', backref ='venue')


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue= db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    past_shows=db.Column(db.String(120))
    past_show_count= db.Column(db.Integer, default = 0)
    upcoming_shows=db.Column(db.String(120))
    upcoming_shows_count=db.Column(db.Integer, default = 0)
    genres = db.relationship('Genres', backref ='artist')

class Genres(db.Model):
    __tablename__='Genre'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(), nullable = False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    artist_id = db.Column(db.Integer,db.ForeignKey('Artist.id'))



class Shows(db.Model):
    __tablename__='Shows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)


