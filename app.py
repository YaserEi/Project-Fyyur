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
import datetime
from datetime import date
from models import app, db, Venue, Artist, Shows, Genres
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#




app.config.from_object('config')
moment = Moment(app)
db.init_app(app)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#







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
      venues = Venue.query.filter_by(id=venue_id).first()
      genre = Genres.query.filter_by(venue_id = venue_id).all()

      show= db.session.query(Artist).join(Shows).values(Shows.start_time, Artist.name,
                       Shows.artist_id, Shows.venue_id, Shows.name, Artist.image_link)
      print(show)

      shows=[]
      print("1")
      for start_time,artist_name,artist_id,show_venue_id,show_name,image_link in show:
          shows.append({
          'start_time': start_time,
          'show name':show_name,
          'artist_id':artist_id,
          'venue_id': show_venue_id,
          'artist_name': artist_name,
          'image_link': image_link
          })

      print(shows)
      #used to update show counts
      upcoming_shows_count=0
      past_shows_count=0

      #used in the HTMl page
      upcoming_shows=[]
      past_shows=[]

      artist=Artist.query.filter_by(id=shows[0]['artist_id']).first()

      # Update shows Count
      if shows:  # Check if shows is empty
          for i in range(len(shows)):  # length of shows
              if shows[i]['venue_id'] == venue_id:
                  print(shows[i]['venue_id'])
                  start_date_obj = datetime.datetime.strptime(shows[i]['start_time'], '%Y-%m-%d %H:%M:%S') #convert starttime string to date
                  if (start_date_obj.date() <date.today()):
                      past_shows_count +=1
                      past_shows.append(shows[i])
                  else:
                      upcoming_shows_count+=1
                      upcoming_shows.append(shows[i])
      print(shows)

      venues.upcoming_shows_count=upcoming_shows_count
      venues.past_show_count=past_shows_count

      db.session.commit()


      for i in range(len(genre)):
          genres.append(genre[i].genre)

      for i in range(len(genre)):
          genres.append(genre[i].genre)
  except:
      print(sys.exc_info())
  finally:
      return render_template('pages/show_venue.html', venue=venues,
       genres=genres, shows=shows,upcoming_shows=upcoming_shows, past_shows=past_shows, artist=artist)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    name_exists = False

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
          website_link=request.form.get('website_link')
          seeking_description=request.form.get('seeking_description')
          venue = Venue(name = name, city = city, state = state,address = address,
          phone = phone_num,seeking_description = seeking_description, image_link=image_link, website_link=website_link, facebook_link = fb_link)
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

          print('name exists')
    except:
      db.session.rollback()
    finally:
      db.session.close()
      if name_exists == False:
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
        artist = Artist.query.filter_by(id=artist_id).first()
        genre = Genres.query.filter_by(artist_id = artist_id).all()
        show= db.session.query(Venue).join(Shows).values(Shows.start_time, Venue.name,
                                        Shows.artist_id, Shows.venue_id, Shows.name, Venue.image_link)

        print(show)
        shows=[]
        for start_time,venue_name,show_artist_id,venue_id,show_name,image_link in show:
            shows.append({
                'start_time': start_time,
                'show name':show_name,
                'artist_id':show_artist_id,
                'venue_id': venue_id,
                'venue_name': venue_name,
                'image_link': image_link
                })

        upcoming_shows_count=0
        past_shows_count=0

        upcoming_shows=[]
        past_shows=[]

        if shows:  # Check if shows is empty
            for i in range(len(shows)):  # length of shows
                if shows[i]['artist_id'] == artist_id:  # make sure the artist id is the one being passed
                    start_date_obj = datetime.datetime.strptime(shows[i]['start_time'], '%Y-%m-%d %H:%M:%S') #convert starttime string to date
                    if (start_date_obj.date() <date.today()):
                        past_shows_count +=1
                        past_shows.append(shows[i])
                    else:
                        upcoming_shows_count+=1
                        upcoming_shows.append(shows[i])


        artist.upcoming_shows_count=upcoming_shows_count
        artist.past_show_count=past_shows_count

        db.session.commit()


        for i in range(len(genre)):
            genres.append(genre[i].genre)

    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        return render_template('pages/show_artist.html', artist=artist, genres=genres, upcoming_shows=upcoming_shows, past_shows=past_shows)
        db.session.close()

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
 seeking = False

 try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')

    existing_name= Artist.query.filter_by(name = name).all()
    existing_city=Artist.query.filter_by(city = city).all()
    existing_state=Artist.query.filter_by(state = state).all()

    if not existing_name:
        phone_num = request.form.get('phone')
        fb_link = request.form.get('facebook_link')
        image_link = request.form.get('image_link')
        genres = request.form.getlist('genres')
        website_link = request.form.get('website_link')
        seeking_description = request.form.get('seeking_description')
        seeking_venue = request.form.getlist('seeking_venue')
        print(seeking_venue)
        if seeking_venue[0] =="Yes":
            print("True")
            seeking = True
        artist = Artist(name=name, city=city, state=state, phone=phone_num,
        image_link=image_link, facebook_link=fb_link, website_link = website_link,
        seeking_description= seeking_description, seeking_venue=seeking)

        db.session.add(artist)
        db.session.commit() # to create Artist ID


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
    if name_exists == False:
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
  data=[]
  shows = Shows.query.all()

  for i in range(len(shows)):
     venue = Venue.query.filter_by(id = shows[i].venue_id).first()
     artist =Artist.query.filter_by(id=shows[i].artist_id).first()

     data.append({
    "venue_id": shows[i].venue_id,
    "venue_name": venue.name,
    "artist_id": artist.id,
    "artist_name": artist.name,
    "artist_image_link": artist.name,
    "start_time": shows[i].start_time,
    "artist_image_link": artist.image_link
  })
  print(data)
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
    name = request.form.get('name')

    venue = Venue.query.filter_by(id = venue_id).first()
    artist = Artist.query.filter_by(id = artist_id).first()


    if venue and artist:
        show = Shows(venue_id=venue_id, artist_id=artist_id, start_time=start_time, name=name)


        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    elif not venue and not artist:
        flash('Show was not listed, invalid venue and artist ids')
    elif not venue:
        flash('Show was not listed, Venue id does not exist')
    elif not artist:
        flash('Show was not listed, Artist id does not exist')
  except:
    print("error")
    flash('Show was not listed')
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
