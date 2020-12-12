import pytest
import psycopg2

from api.src.models import State, City, Zipcode, Venue, Location
from api.src.db import save, drop_all_tables
test_conn = psycopg2.connect(database = 'foursquare_test', user = 'postgres', password = 'postgres')
test_cursor = test_conn.cursor()

@pytest.fixture()
def clean_tables():
    drop_all_tables(test_conn, test_cursor)
    yield
    drop_all_tables(test_conn, test_cursor)

@pytest.fixture()
def city():
    drop_all_tables(test_conn, test_cursor)

    new_york = save(State(name = 'New York'), test_conn, test_cursor)
    pennsylvania = save(State(name = 'Pennsylvania'), test_conn, test_cursor)

    brooklyn = save(City(name='Brooklyn', state_id = new_york.id), test_conn, test_cursor)
    manhattan = save(City(name='Manhattan', state_id = new_york.id), test_conn, test_cursor)
    philadelphia = save(City(name='Philadelphia', state_id = pennsylvania.id), test_conn, test_cursor)
    south_philly_zip = save(Zipcode(code=19019, city_id = philadelphia.id), test_conn, test_cursor)
    chelsea_zip = save(Zipcode(code=10001, city_id = manhattan.id), test_conn, test_cursor)
    gramercy_zip = save(Zipcode(code=10010, city_id = manhattan.id), test_conn, test_cursor)
    dumbo_zip = save(Zipcode(code=11210, city_id = brooklyn.id), test_conn, test_cursor)

    venue = save(Venue(name='Los Tacos Al Pastor', price = 1), test_conn, test_cursor)
    location = save(Location(longitude = 40.7024 , latitude = -73.9875,
        address='141 Front Street', zipcode_id = dumbo_zip.id, venue_id = venue.id), test_conn, test_cursor)
    yield manhattan
    drop_all_tables(test_conn, test_cursor)

def test_zipcodes(city):
    codes = [zipcode.code for zipcode in city.zipcodes(test_cursor)]
    assert codes == [10001, 10010]

def test_state(city):
    city.state(test_cursor).name == 'New York'
