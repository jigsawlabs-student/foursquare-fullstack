from flask import Flask
from .db import get_db
from .orm import *
from .category import Category
from .venue import Venue

import simplejson as json


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
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM venues;')
        records = cursor.fetchall()
        venues = build_from_records(Venue, records)
        venue_dicts = [venue.__dict__ for venue in venues]
        return json.dumps(venue_dicts, default = str)

    @app.route('/venues/<id>')
    def restaurant(id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM venues WHERE id = %s;', (id,))
        record = cursor.fetchone()
        venue = build_from_record(Venue, record)

        return json.dumps(venue.__dict__, default = str)

    @app.route('/categories')
    def categories():
        conn = get_db()
        cursor = conn.cursor()
        categories = find_all(Category, cursor)
        category_dicts = [category.__dict__ for category in categories]
        return json.dumps(category_dicts, default = str)

    @app.route('/categories/<id>')
    def category(id):
        conn = get_db()
        cursor = conn.cursor()
        category = find(Category, id, cursor)

        return json.dumps(category.__dict__, default = str)

    return app


