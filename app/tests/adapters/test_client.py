
from api.src.adapters.client import Client
# Here we'll test our Client class.  This class is responsible for making a 
# request to the foursquare api.  It has the following features.

# 1. Class variables of CLIENT_ID, CLIENT_SECRET, 
# DATE (for the version required in the api), and URL for the root url.

# The first set of tests below check for this.  Get them passing.

def request_venue():
    client = Client()
    venue_id = '5b2932a0f5e9d70039787cf2'
    fsquare_venue = client.request_venue(venue_id)
    assert sorted(list(fsquare_venue.keys())) == ['allowMenuUrlEdit', 'attributes', 
'beenHere', 'bestPhoto', 'canonicalUrl', 'categories', 'colors',
 'contact', 'createdAt', 'defaultHours', 'delivery', 'dislike',
 'hereNow', 'hours', 'id', 'inbox', 'likes', 'listed',
 'location', 'name', 'ok', 'pageUpdates', 'photos', 'popular', 
'price', 'rating', 'ratingColor', 'ratingSignals', 'reasons', 
'seasonalHours', 'shortUrl', 'specials', 'stats', 'timeZone', 
'tips', 'url', 'verified']

