from flask import Flask
import simplejson as json
from flask import request

import api.src.models as models
import api.src.db as db

def create_app(database='foursquare_development', testing = False, debug = True):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=database,
        DEBUG = debug,
        TESTING = testing
    )

    @app.route('/')
    def root_url():
        return 'Welcome to the foursquare api'

    @app.route('/venues')
    def venues():
        conn = db.get_db()
        cursor = conn.cursor()

        venues = db.find_all(models.Venue, cursor)
        venue_dicts = [venue.__dict__ for venue in venues]
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


