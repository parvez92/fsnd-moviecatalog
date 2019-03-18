#!/usr/bin/env python3
from flask import (Flask,
                   render_template,
                   url_for,
                   request,
                   redirect,
                   jsonify,
                   make_response,
                   flash)
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataBase_Setup import UserDetails, MovieCategory, MovieDetails, Base
from flask import session as login_session
import random
import string
import json
import httplib2
import requests
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())[
    'web']['client_id']

# Connect to Database
engine = create_engine('sqlite:///catalogformovies.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# # User Helper Functions


def createUser(login_session):
    newUser = UserDetails(users_name=login_session['username'],
                          users_email=login_session['email'],
                          users_image=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(UserDetails).filter_by(
        users_email=login_session['email']).one()
    return user.users_id


def getUserInfo(user_id):
    user = session.query(UserDetails).filter_by(users_id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(UserDetails).filter_by(users_email=email).one()
        return user.users_id
    except Exception:
        return None


'''

Decarator for checking whether the user is
logged in or not
'''


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash('You are not allowed to access there')
            return redirect('/login')
    return decorated_function


@app.route('/')
@app.route('/catalog')
def showGenres():
    # Get all Genres and Movies
    movie_Categories = session.query(MovieCategory).all()

    # Get lastest 5 items added
    movies = session.query(MovieDetails).order_by(
        MovieDetails.id.desc()).limit(5)

    return render_template('catalog.html',
                           moviegenres=movie_Categories, movies=movies)


@app.route('/moviecatalog/<int:genre_id>')
@app.route('/moviecatalog/<int:genre_id>/movies')
def showGenre(genre_id):
    # Get all movie genres
    print genre_id
    movie_Categories = session.query(MovieCategory).all()

    # Get a movie genre
    movie_category = session.query(
        MovieCategory).filter_by(id=genre_id).first()

    # Get genre of movies
    categoryName = movie_category.genre

    # Get all movies of a specific genre
    movies = session.query(MovieDetails).filter_by(
        movie_category_id=genre_id).all()

    # Get count of genres
    moviesPerCategory = session.query(MovieDetails).filter_by(
        movie_category_id=genre_id).count()

    return render_template('genre.html', moviegenres=movie_Categories,
                           movies=movies, movieName=categoryName,
                           moviesPerGenre=moviesPerCategory)


@app.route('/moviecatalog/<int:genre_id>/movie/<int:movie_id>')
def showMovie(genre_id, movie_id):
    # Get movie details
    movieDetails = session.query(MovieDetails).filter_by(id=movie_id).first()

    # Get user details for movie
    creator = getUserInfo(movieDetails.users_id)

    return render_template('movieDetails.html',
                           moviedetails=movieDetails, creator=creator)


@app.route('/movie/add', methods=['GET', 'POST'])
def addMovie():
    if request.method == 'POST':

        if not request.form['name']:
            flash('Please add movie name')
            return redirect(url_for('addMovie'))

        if not request.form['description']:
            flash('Please add a description')
            return redirect(url_for('addMovie'))

        # Add Movie
        newMovie = MovieDetails(name=request.form['name'],
                                description=request.form['description'],
                                movie_category_id=request.form['genre'],
                                users_id=login_session['user_id'])
        session.add(newMovie)
        session.commit()
        flash('Movie Added Successfully')

        return redirect(url_for('showGenres'))
    else:
        # Get all Genres
        genres = session.query(MovieCategory).all()

        return render_template('addMovie.html', genres=genres)


@app.route('/genre/add', methods=['GET', 'POST'])
def addGenre():
    if request.method == 'POST':

        if not request.form['genre']:
            flash('Please add genre name')
            return redirect(url_for('addGenre'))

        # Add Genre
        genres = session.query(MovieCategory).filter_by(
            genre=request.form['genre'].capitalize()).first()
        if genres is None:
            newGenre = MovieCategory(genre=request.form['genre'].capitalize(),
                                     users_id=login_session['user_id'])
            session.add(newGenre)
            session.commit()
            flash('Genre Added Successfully')
            return redirect(url_for('showGenres'))
        else:
            flash('Genre Already Exists')
            return redirect(url_for('addGenre'))

    else:
        # Get all Genres
        genres = session.query(MovieCategory).all()

        return render_template('addGenre.html', genres=genres)


@app.route('/catalog/<int:genre_id>/movies/<int:movie_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editMovie(genre_id, movie_id):
    # Get Movie
    movie = session.query(MovieDetails).filter_by(id=movie_id).first()

    # Get creator of item
    creator = getUserInfo(movie.users_id)

    # Check if logged in user is creator of movie
    if creator.users_id != login_session['user_id']:
        return redirect('/login')

    # Get all genres
    genres = session.query(MovieCategory).all()

    if request.method == 'POST':
        if not request.form['name']:
            flash('Please add movie name')
            return redirect(url_for('editMovie',
                                    genre_id=movie.movie_category_id,
                                    movie_id=movie.id))

        if not request.form['description']:
            flash(
                'Movie Description was not provided showing previous desc')
            return redirect(url_for('editMovie',
                                    genre_id=movie.movie_category_id,
                                    movie_id=movie.id))

        if (movie.name == request.form['name'] and
                movie.description == request.form['description'] and
                str(movie.movie_category_id) == request.form['genre']):
            flash(
                'No changes were made as previous values were provided')
            return redirect(url_for('editMovie',
                                    genre_id=movie.movie_category_id,
                                    movie_id=movie.id))

        if request.form['name']:
            movie.name = request.form['name']
        if request.form['description']:
            movie.description = request.form['description']
        if request.form['genre']:
            movie.movie_category_id = request.form['genre']
        session.add(movie)
        session.commit()
        flash('Movie Updated Successfully')
        return redirect(url_for('showMovie',
                                genre_id=movie.movie_category_id,
                                movie_id=movie.id))
    else:
        return render_template('editMovie.html', genres=genres, movies=movie)


@app.route('/catalog/<int:genre_id>/items/<int:movie_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteMovie(genre_id, movie_id):
    # Get movie
    movie = session.query(MovieDetails).filter_by(id=movie_id).first()

    # Get creator of movie
    creator = getUserInfo(movie.users_id)

    # Check if logged in user is creator of movie
    if creator.users_id != login_session['user_id']:
        return redirect('/login')

    if request.method == 'POST':
        session.delete(movie)
        session.commit()
        flash('Movie Deleted Successfully')
        return redirect(url_for('showGenre', genre_id=movie.movie_category_id))
    else:
        return render_template('deleteMovie.html', movies=movie)


@app.route('/login')
def login():
    if 'username' in login_session:
        return redirect('/')
    # Creating AntiForgery state token
    else:
        state = ''.join(random.choice(string.ascii_uppercase +
                                      string.digits) for x in xrange(32))
        login_session['state'] = state

        return render_template('login.html', STATE=state)


@app.route('/logout')
def logout():
    if login_session['provider'] == 'facebook':
        fbdisconnect()
        del login_session['facebook_id']

    if login_session['provider'] == 'google':
        gdisconnect()
        del login_session['gplus_id']
        del login_session['access_token']

    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['provider']

    return redirect(url_for('showGenres'))


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    # Validate anti-forgery state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Get acces token
    access_token = request.data
    print "access token received %s " % access_token

    # Gets info from fb clients secrets
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_secret']

    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)  # NOQA
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"

    # strip expire tag from access token
    token = json.loads(result)['access_token']

    url = 'https://graph.facebook.com/v2.4/me?access_token=%s&fields=name,id,email' % token  # NOQA
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # Store token in login_session in order to logout
    stored_token = token
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?access_token=%s&redirect=0&height=200&width=200' % token  # NOQA
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # See if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    return "Login Successful!"


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']

    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]

    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate anti-forgery state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            "Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            "Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # See if user exists
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    return "Login Successful"


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')

    if access_token is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(json.dumps(
            'Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/moviecatalog/JSON')
def showgenresJSON():
    moviegenres = session.query(MovieCategory).all()
    return jsonify(moviegenres=[genre.serialize for genre in moviegenres])


@app.route('/moviecatalog/<int:genre_id>/JSON')
@app.route('/moviecatalog/<int:genre_id>/movies/JSON')
def showMoviesIngenreJSON(genre_id):
    moviesIngenre = session.query(MovieDetails).filter_by(
        movie_category_id=genre_id).all()
    return jsonify(moviesIngenre=[moviedetail.serialize
                                  for moviedetail in moviesIngenre])


@app.route('/moviecatalog/<int:genre_id>/movie/<int:movie_id>/JSON')
def showMovieDetailsJSON(genre_id, movie_id):
    movie = session.query(MovieDetails).filter_by(id=movie_id).first()
    return jsonify(movieDetails=[movie.serialize])

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
