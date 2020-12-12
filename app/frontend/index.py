import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
API_URL = "http://127.0.0.1:5000/venues/search"


def find_venues(price):
    response = requests.get(API_URL, params = {'price': price})
    return response.json()


def venue_names(venues, requires_rating = False):
    if requires_rating:
        venues = [venue for venue in venues if venue['rating'] != -99]
    return [venue['name'] for venue in venues]

def venue_ratings(venues, requires_rating = False):
    if requires_rating:
        venues = [venue for venue in venues if venue['rating'] != -99]
    return [venue['rating'] for venue in venues]


price = st.sidebar.slider(min_value = 1, max_value = 2, step = 1, label = 'price')
st.header('Venues')
venues = find_venues(price)

def venue_locations(venues):
    return [venue['location'] for venue in venues if venue.get('location') ]


scatter = go.Scatter(x = venue_names(venues, True), 
        y = venue_ratings(venues, True), 
        hovertext = venue_names(venues, True), mode = 'markers')

locations = venue_locations(venues)


fig = go.Figure(scatter)
st.plotly_chart(fig)
st.map(pd.DataFrame(locations))
