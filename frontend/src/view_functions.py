import requests
API_URL = "http://127.0.0.1:5000/venues/search"
CATEGORY_URL = "http://127.0.0.1:5000/categories"

def find_venues(price):
    response = requests.get(API_URL, params = {'price': price})
    return response.json()


def find_categories():
    response = requests.get(CATEGORY_URL)
    return response.json()

def venue_names(venues, requires_rating = False):
    if requires_rating:
        venues = [venue for venue in venues if venue['rating'] != -99]
    return [venue['name'] for venue in venues]

def category_names(categories):
    return [category['name'] for category in categories]

def category_ratings(categories):
    return [category['rating'] for category in categories]

def venue_ratings(venues, requires_rating = False):
    if requires_rating:
        venues = [venue for venue in venues if venue['rating'] != -99]
    return [venue['rating'] for venue in venues]

def venue_locations(venues):
    return [venue['location'] for venue in venues if venue.get('location') ]

def category_colors(venues):
    categories = [venue.get('category', 'other') for venue in venues]
    color_map = {'Mexican Restaurant': 'blue', 'Pizza Place': 'red', 'Italian': 'green', 'Bar': 'orange', 'Taco Place': 'yellow', "Food Truck": "purple"}
    colors = [color_map.get(category, 'gray') for category in categories]
    return colors

def venue_likes_and_names(venues):
    likes = [venue['likes'] for venue in venues if venue.get('likes')]
    names = [venue['name'] for venue in venues if venue.get('name')]
    return (likes, names)
