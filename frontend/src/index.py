import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from view_functions import (find_venues, venue_names, 
venue_ratings, venue_locations, venue_likes_and_names, find_categories, category_names, category_ratings, category_colors)


price = st.sidebar.slider(min_value = 1, max_value = 2, step = 1, label = 'price')
venues = find_venues(price)
categories = find_categories()

st.write('Categories')
scatter = go.Scatter(x = category_names(categories), y = category_ratings(categories), mode = 'markers')
fig = go.Figure(scatter)
st.plotly_chart(fig)

st.header('Venues')
st.write('Venue ratings')
colors = category_colors(venues)
scatter = go.Scatter(x = venue_names(venues, True), y = venue_ratings(venues, True), marker = {'color': colors }, mode = 'markers')
fig = go.Figure(scatter)
st.plotly_chart(fig)

st.write('Venue Likes')
likes_and_names = venue_likes_and_names(venues)
likes_scatter = go.Scatter(x = likes_and_names[1], y = likes_and_names[0], mode = 'markers') 
likes_fig = go.Figure(likes_scatter)


st.plotly_chart(likes_fig)
locations = venue_locations(venues)
st.map(pd.DataFrame(locations))
