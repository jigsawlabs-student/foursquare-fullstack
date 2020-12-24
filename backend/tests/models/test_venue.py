import pytest
from api.src.models import State, City, Zipcode, Venue, Location, Category, VenueCategory
from api.src.db.db import save, drop_all_tables, get_db, find_all, find, close_db
from api.src import create_app


def build_records(test_conn, test_cursor):
    new_york = save(State(name = 'New York'), test_conn, test_cursor)
    pennsylvania = save(State(name = 'Pennsylvania'), test_conn, test_cursor)

    brooklyn = save(City(name='Brooklyn', state_id = new_york.id), test_conn, test_cursor)
    manhattan = save(City(name='Manhattan', state_id = new_york.id), test_conn, test_cursor)
    philadelphia = save(City(name='Philadelphia', state_id = pennsylvania.id), test_conn, test_cursor)
    south_philly_zip = save(Zipcode(code=19019, city_id = philadelphia.id), test_conn, test_cursor)
    chelsea_zip = save(Zipcode(code=10001, city_id = manhattan.id), test_conn, test_cursor)
    dumbo_zip = save(Zipcode(code=11210, city_id = brooklyn.id), test_conn, test_cursor)

    venue = save(Venue(name='Los Tacos Al Pastor', price = 1, foursquare_id = '1234'), test_conn, test_cursor)
    grimaldis = save(Venue(name='Grimaldis', price = 2, foursquare_id = '4bf58dd8d48988d151941735'), test_conn, test_cursor)
    pizza = save(Category(name='Pizza'), test_conn, test_cursor)
    tourist_spot = save(Category(name='Tourist Spot'), test_conn, test_cursor)
    save(VenueCategory(venue_id = grimaldis.id, category_id = pizza.id), test_conn, test_cursor)
    save(VenueCategory(venue_id = grimaldis.id, category_id = tourist_spot.id), test_conn, test_cursor)

    grimaldi_location = save(Location(longitude = 40.7024 , latitude = -73.9875,
        address='1 Front Street', zipcode_id = dumbo_zip.id, venue_id = grimaldis.id), test_conn, test_cursor)
    taco_location = save(Location(longitude = 40.7024 , latitude = -73.9875,
        address='141 Front Street', zipcode_id = dumbo_zip.id, venue_id = venue.id), test_conn, test_cursor)
    zahav = save(Venue(foursquare_id = '9912', name = 'Zahavs',
        price = 4, rating = 5, likes = 100, menu_url = 'zahavs.com'), test_conn, test_cursor)
    save(Location(longitude = 40.7024 , latitude = -73.9875,
        address='237 James Street', zipcode_id = south_philly_zip.id, 
        venue_id = zahav.id), test_conn, test_cursor)

@pytest.fixture()
def db_cursor():
    flask_app = create_app()
    flask_app.config['DATABASE'] = 'foursquare_test'

    with flask_app.app_context():
        conn = get_db()
        cursor = conn.cursor()

    drop_all_tables(conn, cursor)
    build_records(conn, cursor)
    yield cursor
    with flask_app.app_context():
        close_db()
        conn = get_db()
        cursor = conn.cursor()
        drop_all_tables(conn, cursor)
        close_db()

def test_venue_location(db_cursor):
    foursquare_id = "4bf58dd8d48988d151941735"
    grimaldis = Venue.find_by_foursquare_id(foursquare_id, db_cursor)
    assert grimaldis.location(db_cursor).address == '1 Front Street'

def test_find_by_foursquare_id(db_cursor):
    foursquare_id = "4bf58dd8d48988d151941735"
    assert Venue.find_by_foursquare_id(foursquare_id, db_cursor).name == 'Grimaldis'

def test_venue_categories(db_cursor):
    foursquare_id = "4bf58dd8d48988d151941735"
    grimaldis = Venue.find_by_foursquare_id(foursquare_id, db_cursor)
    categories = grimaldis.categories(db_cursor)
    category_names = [category.name for category in categories]
    assert category_names == ['Pizza', 'Tourist Spot']

def test_category_search(db_cursor):
    params = {'category': 'Pizza'}
    found_venues = Venue.search(params, db_cursor)
    assert 'Grimaldis' == found_venues[0].name

def test_state_search(db_cursor):
    params = {'state': 'Pennsylvania'}
    found_venues = Venue.search(params, db_cursor)
    assert 'Zahavs' == found_venues[0].name
