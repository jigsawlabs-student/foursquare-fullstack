from flask import Flask, jsonify
from .db import get_db
import simplejson as json


def create_app(database='squawk_development', testing = False, debug = True):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=database,
        DEBUG = debug,
        TESTING = testing
    )

    @app.route('/')
    def root_url():
        return 'Welcome to squawk'

    @app.route('/first')
    def first():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM restaurants ORDER BY id ASC LIMIT 1;')
        record = cursor.fetchone()
        return json.dumps(record, default=str)

    @app.route('/restaurants')
    def restaurants():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM restaurants;')
        records = cursor.fetchall()
        return json.dumps(records, default = str)

    @app.route('/restaurants/<id>')
    def restaurant(id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM restaurants WHERE id = %s;', (id,))
        records = cursor.fetchall()
        return json.dumps(records, default = str)

    return app


