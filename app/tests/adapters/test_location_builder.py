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
def test_db():
    test_conn = psycopg2.connect(dbname = 'foursquare_test', 
            user = 'postgres', password = 'postgres')
    cursor = test_conn.cursor()
    db.drop_all_tables(test_conn, cursor)
    yield test_conn
    db.drop_all_tables(test_conn, cursor)



def test_find_or_create_by_city_state_zip(test_db):
    city_name, state_name, zipcode_code = 'Newark', 'New Jersey', 12345
    builder = adapters.LocationBuilder()
    cursor = test_db.cursor()

    builder.find_or_create_by_city_state_zip(city_name, state_name, zipcode_code, test_db, cursor)
    new_jersey = db.find_by_name(models.State, 'New Jersey', cursor)
    newark = db.find_by_name(models.City, 'Newark', cursor)
    zipcode = models.Zipcode.find_by_code(12345, cursor)
    assert zipcode.city_id == newark.id
    assert newark.state_id == new_jersey.id
    assert new_jersey.name == 'New Jersey'

def test_find_or_create_by_finds_city_state_where_exists(test_db):
    cursor = test_db.cursor()
    city_name, state_name, zipcode_code = 'Newark', 'New Jersey', 12345
    builder = adapters.LocationBuilder()

    city, state, zipcode = builder.find_or_create_by_city_state_zip(city_name, state_name, zipcode_code, test_db, cursor)
    # Same data but different zip code

    zipcode = models.Zipcode.find_by_code(11111, cursor)
    new_city, new_state, new_zip = builder.find_or_create_by_city_state_zip(city_name, state_name, zipcode_code, test_db, cursor)

    assert new_city.id == city.id
    assert new_state.id == state.id
    assert new_zip.city_id == city.id

def test_build_location_city_state_zip(test_db):
    select_attr = {'address': '141 Front St', 'lat': 40.70243624175102, 
            'lng': -73.98753900608666, 'postalCode': '11201', 
            'city': 'New York', 'state': 'NY'}
    cursor = test_db.cursor()
    builder = adapters.LocationBuilder()

    location = builder.build_location_city_state_zip(select_attr, test_db, cursor)
    new_york = db.find_by_name(models.State, 'New York', cursor)
    nyc = db.find_by_name(models.City, 'New York', cursor)
    zipcode = models.Zipcode.find_by_code('11201', cursor)
    location.zipcode = zipcode.id

def test_select_location_attributes():
    lb = adapters.LocationBuilder()
    assert lb.select_attributes(venue_details) == {'address': '141 Front St', 
            'lat': 40.70243624175102, 'lng': -73.98753900608666, 'postalCode': '11201', 
            'city': 'New York', 'state': 'NY'}
    


