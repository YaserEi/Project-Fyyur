#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app,db)
moment = Moment(app)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#




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

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

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
    website = db.Column(db.String(120))
    seeking_venue= db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    past_shows=db.Column(db.String(120))
    past_show_count= db.Column(db.Integer)
    upcoming_shows=db.Column(db.String(120))
    upcoing_shows_count=db.Column(db.Integer)
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


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  venues = Venue.query.distinct("state","city").all()
  for i in range(len(venues)):
      venues_state=Venue.query.filter_by(state= venues[i].state, city=venues[i].city).all()
      for x in range(len(venues_state)):
          venues_common= Venue.query.filter_by(city=venues_state[x].city).all()
          data.append({
            "city": venues_common[x].city + ",",
            "state": venues_state[x].state,
            "venues": [{
              "id": venues_state[x].id,
              "name": venues_state[x].name
            }]
          })
  for y in range((len(data)-1),0,-1):
    if data[y]["city"] == data[y-1]["city"] and data[y]["state"] == data[y-1]['state']:
        del data[y]["city"]
        del data[y]["state"]

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term')
  search_results = Venue.query.filter(Venue.name.ilike('%'+search_term+'%')).all()
  search_count=len(search_results)


  return render_template('pages/search_venues.html', results=search_results, search_term=request.form.get('search_term', ''), count=search_count)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  try:
      genres=[]
      venues = Venue.query.filter_by(id=venue_id).all()
      genre = Genres.query.filter_by(venue_id = venue_id).all()
      for i in range(len(genre)):
          genres.append(genre[i].genre)
  except:
      print(sys.exc_info())
  finally:
      return render_template('pages/show_venue.html', venue=venues[0], genres=genres)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    name_exists = False
    state_exists = False
    city_exists = False
    address_exists = False
    try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      address = request.form.get('address')


      existing_name = Venue.query.filter_by(name = name).all()

      if len(existing_name)==0:
          phone_num = request.form.get('phone')
          genres = request.form.getlist('genres')
          image_link = request.form.get('image_link')
          fb_link = request.form.get('facebook_link')
          venue = Venue(name = name, city = city, state = state,address = address, phone = phone_num, image_link=image_link, facebook_link = fb_link)
          print("name doesnt exist")
          db.session.add(venue)
          db.session.commit()

         #Adding Genres to Genre table
         #Two commits to add venue ID
          for i in range(len(genres)):
              genre = Genres(genre = genres[i], venue_id = venue.id)
              db.session.add(genre)
          db.session.commit()
      else:
          name_exists = True
          state_exists = True
          city_exists = True
          address_exists = True
          print('name exists')
    except:
      db.session.rollback()
    finally:
      db.session.close()
      if name_exists == False and state_exists ==False and city_exists==False and address_exists==False:
          flash('Venue ' + request.form['name']+ ' was successfully listed!')
      else:
          flash('Venue ' + request.form['name']+ ' was not listed, venue name exists')
      return redirect(url_for('index'))

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    genres = Genres.query.filter_by(id = venue_id).all()

    for i in range(len(genres)):
        db.session.delete(genres[i])

    db.session.delete(venue)
    db.session.commit()
  except:
    print(sys.exc_info())
    print("error")
    db.session.rollback()
  finally:
    print("finally")
    db.session.close()


  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
    data = []
    artists = Artist.query.all()
    for i in range(len(artists)):
            data.append({
              "id": artists[i].id,
              "name": artists[i].name,
            })

    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():

  search_term = request.form.get('search_term')
  search_results = Artist.query.filter(Artist.name.ilike('%'+search_term+'%')).all()
  search_count=len(search_results)
  return render_template('pages/search_artists.html', results=search_results, search_term=request.form.get('search_term', ''), count=search_count)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

    try:
        genres=[]
        artists = Artist.query.filter_by(id=artist_id).all()
        genre = Genres.query.filter_by(artist_id = artist_id).all()
        for i in range(len(genre)):
            genres.append(genre[i].genre)
    except:
        print(sys.exc_info())
    finally:
        return render_template('pages/show_artist.html', artist=artists[0], genres=genres)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist=Artist.query.filter_by(id=artist_id).all()

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist[0])

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      phone = request.form.get('phone_num')
      facebook_link = request.form.get('facebook_link')

      artist=Artist.query.filter_by(id=artist_id).first()
      artist.name = name
      artist.city = city
      artist.state = state
      artist.phone = phone
      artist.facebook_link = facebook_link


      db.session.commit()
    except:
      db.session.rollback()
      print("error")
      print(sys.exc_info())
    finally:
      db.session.close()


    return redirect(url_for('show_artist', artist_id=artist_id))



@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue=Venue.query.filter_by(id=venue_id).first()

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      phone = request.form.get('phone_num')
      facebook_link = request.form.get('facebook_link')

      venue=Venue.query.filter_by(id=venue_id).first()
      venue.name = name
      venue.city = city
      venue.state = state
      venue.phone = phone
      venue.facebook_link = facebook_link
      #venue.upcoming_shows = "none"

      db.session.commit()
    except:
      db.session.rollback()
      print("error")
      print(sys.exc_info())
    finally:
      db.session.close()

  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
 name_exists = False
 state_exists = False
 city_exists = False
 try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')

    existing_name= Artist.query.filter_by(name = name).all()
    existing_city=Artist.query.filter_by(city = city).all()
    existing_state=Artist.query.filter_by(state = state).all()

    if not existing_name and not existing_city and not existing_state:
        phone_num = request.form.get('phone')
        fb_link = request.form.get('facebook_link')
        image_link = request.form.get('image_link')
        genres = request.form.getlist('genres')
        artist = Artist(name=name, city=city, state=state, phone=phone_num, image_link=image_link, facebook_link=fb_link)
        db.session.add(artist)
        db.session.commit()

        for i in range(len(genres)):
            genre = Genres(genre=genres[i], artist_id=artist.id)
            db.session.add(genre)
        db.session.commit()
    else:
         name_exists = True
         state_exists = True
         city_exists = True

 except:
    print("error")
    db.session.rollback()
 finally:
    print("finally")
    db.session.close()

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
    if name_exists == False and state_exists ==False and city_exists==False:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
        flash('Artist ' + request.form['name'] + ' was not listed, artist already exists')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
    venue_id = request.form.get('venue_id')
    artist_id = request.form.get('artist_id')
    start_time = request.form.get('start_time')

    venue = Venue.query.filter_by(id = venue_id).all()
    artist = Artist.query.filter_by(id = artist_id).all()


    if venue and artist:
        show = Shows(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    elif not venue and not artist:
        flash('Show was not listed, invalid venue and artist ids')
    elif not venue:
        print('venue')
        flash('Show was not listed, Venue id does not exist')
    elif not artist:
        print('artist')
        flash('Show was not listed, Artist id does not exist')
  except:
    print("error")
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()

    print(sys.exc_info())

  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:


# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
