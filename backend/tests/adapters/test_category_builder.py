import psycopg2
import pytest
from decimal import *
import api.src.db.db as db
import api.src.models as models
import api.src.adapters as adapters
from tests.adapters.venue_details import venue_details

location =  {'address': '141 Front St', 'crossStreet': 'Pearl St', 'lat': 40.70243624175102, 'lng': -73.98753900608666, 'labeledLatLngs': [{'label': 'display', 'lat': 40.70243624175102, 'lng': -73.98753900608666}], 'postalCode': '11201', 'cc': 'US', 'neighborhood': 'DUMBO', 'city': 'New York', 'state': 'NY', 
        'country': 'United States', 'formattedAddress': ['141 Front St (Pearl St)', 'New York, NY 11201', 'United States']}

categories = [{'id': '4bf58dd8d48988d151941735', 'name': 'Taco Place', 'pluralName': 'Taco Places', 'shortName': 'Tacos', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/taco_', 'suffix': '.png'}, 'primary': True}]

venue_details = {'id': '5b2932a0f5e9d70039787cf2', 'name': 'Los Tacos Al Pastor', 'categories': categories, 'location': location, 'rating': 7.9, 'price': {'tier': 1}, 'likes': {'count': 52}, 
        'delivery': {'url': 'https://www.seamless.com/menu/los-tacos-al-pastor-141a-front-st-brooklyn/857049?affiliate=1131&utm_source=foursquare-affiliate-network&utm_medium=affiliate&utm_campaign=1131&utm_content=857049'}}


@pytest.fixture()
def conn():
    test_conn = psycopg2.connect(dbname = 'foursquare_test', 
            user = 'postgres', password = 'postgres')
    cursor = test_conn.cursor()
    db.drop_all_tables(test_conn, cursor)
    yield test_conn
    db.drop_all_tables(test_conn, cursor)

def test_select_category_attributes():
    cb = adapters.CategoryBuilder()
    category_attr = cb.select_attributes(venue_details)

def test_find_or_create_by_creates_when_new_category(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM categories;')
    begin_cat_num = cursor.fetchone()
    cb = adapters.CategoryBuilder()

    cb.find_or_create_categories(['Taco Places'], conn, cursor)
    cursor.execute('SELECT COUNT(*) FROM categories;')
    end_cat_num = cursor.fetchone()
    assert end_cat_num[0] == begin_cat_num[0] + 1

def test_find_or_create_by_finds_when_existing_category(conn):
    cursor = conn.cursor()
    cb = adapters.CategoryBuilder()
    category = db.save(models.Category(name = 'Taco Places'), conn, cursor)
    new_categories = cb.find_or_create_categories(['Taco Places'], conn, cursor)
    assert category.id == new_categories[0].id

