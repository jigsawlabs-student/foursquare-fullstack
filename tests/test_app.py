import pytest
from src import app

@pytest.fixture(scope='module')
def client():
    flask_app = app
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()

def test_root_url(client):
    response = client.get('/')
    assert b'Welcome to Squawk' in response.data

def test_restaurants(client):
    response = client.get('/restaurants')
    assert b'chipotle, sweetgreen, and five guys' in response.data
