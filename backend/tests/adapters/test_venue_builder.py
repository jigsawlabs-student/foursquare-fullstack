import psycopg2
import pytest
from decimal import *
import api.src.db.db as db
import api.src.models as models
import api.src.adapters as adapters


location =  {'address': '141 Front St', 'crossStreet': 'Pearl St', 'lat': 40.70243624175102, 'lng': -73.98753900608666, 'labeledLatLngs': [{'label': 'display', 'lat': 40.70243624175102, 'lng': -73.98753900608666}], 'postalCode': '11201', 'cc': 'US', 'neighborhood': 'DUMBO', 'city': 'New York', 'state': 'NY', 
        'country': 'United States', 'formattedAddress': ['141 Front St (Pearl St)', 'New York, NY 11201', 'United States']}

categories = [{'id': '4bf58dd8d48988d151941735', 'name': 'Taco Place', 'pluralName': 'Taco Places', 'shortName': 'Tacos', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/taco_', 'suffix': '.png'}, 'primary': True}]

venue_details = {'id': '5b2932a0f5e9d70039787cf2', 'name': 'Los Tacos Al Pastor', 'categories': categories, 'location': location, 'rating': 7.9, 'price': {'tier': 1}, 'likes': {'count': 52}, 
        'delivery': {'url': 'https://www.seamless.com/menu/los-tacos-al-pastor-141a-front-st-brooklyn/857049?affiliate=1131&utm_source=foursquare-affiliate-network&utm_medium=affiliate&utm_campaign=1131&utm_content=857049'}}

@pytest.fixture()
def test_conn():
    test_conn = psycopg2.connect(dbname = 'foursquare_test',
            user = 'postgres', password = 'postgres')
    cursor = test_conn.cursor()
    db.drop_all_tables(test_conn, cursor)
    yield test_conn
    db.drop_all_tables(test_conn, cursor)

def test_select_attributes():
    vb = adapters.VenueBuilder()
    selected = vb.select_attributes(venue_details)
    assert selected == {'foursquare_id': '5b2932a0f5e9d70039787cf2',
          'likes': 52,
          'name': 'Los Tacos Al Pastor',
          'price': 1,
          'rating': 7.9,
          'menu_url': 'https://www.seamless.com/menu/los-tacos-al-pastor-141a-front-st-brooklyn/857049'}

def test_run_adds_new_venue_where_does_not_exist(test_conn):
    test_cursor = test_conn.cursor()
    vb = adapters.VenueBuilder()
    venue = vb.run(venue_details, test_conn, test_cursor)

    assert venue.exists == False
    venue_from_db = models.Venue.find_by_foursquare_id('5b2932a0f5e9d70039787cf2', test_cursor)
    assert venue_from_db.foursquare_id == '5b2932a0f5e9d70039787cf2'
    assert venue_from_db.name == 'Los Tacos Al Pastor'

def test_run_returns_existing_venue_where_exists(test_conn):
    test_cursor = test_conn.cursor()
    vb = adapters.VenueBuilder()
    old_venue = vb.run(venue_details, test_conn, test_cursor)

    new_venue = vb.run(venue_details, test_conn, test_cursor)
    assert new_venue.exists == True
    assert old_venue.id == new_venue.id
