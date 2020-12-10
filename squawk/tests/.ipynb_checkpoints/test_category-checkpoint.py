import pytest
from decimal import *

from src import State, City, Zipcode, Venue, Location, Category, VenueCategory, save, find_all, test_conn, test_cursor, drop_all_tables


@pytest.fixture()
def build_category():
    drop_all_tables(test_conn, test_cursor)
    category = Category()
    category.name = 'Taco Places'
    save(category, test_conn, test_cursor)

    yield

    drop_all_tables(test_conn, test_cursor)

@pytest.fixture()
def build_categories():
    drop_all_tables(test_conn, test_cursor)
    category = Category()
    category.name = 'Taco Places'
    save(category, test_conn, test_cursor)

    category = Category()
    category.name = 'Asian Fusion'
    save(category, test_conn, test_cursor)
    yield

    drop_all_tables(test_conn, test_cursor)
@pytest.fixture()
def clean_tables():
    drop_all_tables(test_conn, test_cursor)
    yield

    drop_all_tables(test_conn, test_cursor)


def test_find_by_name(build_category):
    category = Category.find_by_name('Taco Places', test_cursor)
    assert category.name == 'Taco Places'

def test_find_or_create_by_creates_when_new_category(clean_tables):
    test_cursor.execute('SELECT COUNT(*) FROM categories;')
    begin_cat_num = test_cursor.fetchone()

    Category.find_or_create_by_name('Taco Places', test_conn, test_cursor)
    test_cursor.execute('SELECT COUNT(*) FROM categories;')
    end_cat_num = test_cursor.fetchone()
    assert end_cat_num[0] == begin_cat_num[0] + 1


def test_find_or_create_by_finds_when_existing_category(clean_tables):
    category = Category()
    category.name = 'Taco Places'
    save(category, test_conn, test_cursor)

    test_cursor.execute('SELECT COUNT(*) FROM categories;')
    begin_cat_num = test_cursor.fetchone()

    Category.find_or_create_by_name('Taco Places', test_conn, test_cursor)
    test_cursor.execute('SELECT COUNT(*) FROM categories;')
    end_cat_num = test_cursor.fetchone()
    assert end_cat_num == begin_cat_num

def test_find_all(build_categories):
    categories = find_all(Category, test_cursor)
    assert [category.name for category in categories] == ['Taco Places', 'Asian Fusion']

@pytest.fixture()
def tourist_spot():
    drop_all_tables(test_conn, test_cursor)

    new_york = save(State(name = 'New York'), test_conn, test_cursor)
    pennsylvania = save(State(name = 'Pennsylvania'), test_conn, test_cursor)

    brooklyn = save(City(name='Brooklyn', state_id = new_york.id), test_conn, test_cursor)
    manhattan = save(City(name='Manhattan', state_id = new_york.id), test_conn, test_cursor)
    philadelphia = save(City(name='Philadelphia', state_id = pennsylvania.id), test_conn, test_cursor)
    south_philly_zip = save(Zipcode(code=19019, city_id = philadelphia.id), test_conn, test_cursor)
    chelsea_zip = save(Zipcode(code=10001, city_id = manhattan.id), test_conn, test_cursor)
    dumbo_zip = save(Zipcode(code=11210, city_id = brooklyn.id), test_conn, test_cursor)

    venue = save(Venue(name='Los Tacos Al Pastor', price = 1, foursquare_id = '4bf58dd8d48988d151941735'), test_conn, test_cursor)
    grimaldis = save(Venue(name='Grimaldis', price = 2), test_conn, test_cursor)
    pizza = save(Category(name='Pizza'), test_conn, test_cursor)
    tourist_spot = save(Category(name='Tourist Spot'), test_conn, test_cursor)
    save(VenueCategory(venue_id = grimaldis.id, category_id = pizza.id), test_conn, test_cursor)
    save(VenueCategory(venue_id = grimaldis.id, category_id = tourist_spot.id), test_conn, test_cursor)

    save(VenueCategory(venue_id = venue.id, category_id = tourist_spot.id), test_conn, test_cursor)
    grimaldi_location = save(Location(longitude = 40.7024 , latitude = -73.9875,
        address='1 Front Street', zipcode_id = dumbo_zip.id, venue_id = grimaldis.id), test_conn, test_cursor)
    taco_location = save(Location(longitude = 40.7024 , latitude = -73.9875,
        address='141 Front Street', zipcode_id = dumbo_zip.id, venue_id = venue.id), test_conn, test_cursor)
    yield tourist_spot
    drop_all_tables(test_conn, test_cursor)

def test_category_venues(tourist_spot):
    venues = tourist_spot.venues(test_cursor)
    category_names = [venue.name for venue in venues]
    assert category_names == ['Los Tacos Al Pastor', 'Grimaldis']
    
