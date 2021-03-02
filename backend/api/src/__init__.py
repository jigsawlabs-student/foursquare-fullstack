from flask import Flask
import simplejson as json
from flask import request

import api.src.models as models
import api.src.db.db as db
from settings import DB_USER, DB_NAME, DB_HOST, DB_PASSWORD, DEBUG, TESTING

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        DB_USER = DB_USER,
        DB_PASSWORD = DB_PASSWORD,
        DATABASE= DB_NAME,
        DB_HOST = DB_HOST,
        DEBUG = DEBUG,
        TESTING = TESTING
    )

    @app.route('/')
    def root_url():
        return 'Welcome to the foursquare api'

    @app.route('/venues')
    def venues():
        conn = db.get_db()
        cursor = conn.cursor()

        venues = db.find_all(models.Venue, cursor)
        venue_dicts = [venue.to_json(cursor) for venue in venues]
        return json.dumps(venue_dicts, default = str)

    @app.route('/venues/search')
    def search_venues():
        conn = db.get_db()
        cursor = conn.cursor()

        params = dict(request.args)
        venues = models.Venue.search(params, cursor)
        venue_dicts = [venue.to_json(cursor) for venue in venues]
        return json.dumps(venue_dicts, default = str)

    @app.route('/venues/<id>')
    def venue(id):
        conn = db.get_db()
        cursor = conn.cursor()
        venue = db.find(models.Venue, id, cursor)

        return json.dumps(venue.__dict__, default = str)


    return app


