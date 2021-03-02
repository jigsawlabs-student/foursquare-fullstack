import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from view_functions import (find_venues, venue_names, 
venue_ratings, venue_locations, category_colors)


price = st.sidebar.slider(min_value = 1, max_value = 2, step = 1, label = 'price')
venues = find_venues(price)


st.header('Venues')
st.write('Venue ratings')
scatter = go.Scatter(x = venue_names(venues, True), y = venue_ratings(venues, True), mode = 'markers')
fig = go.Figure(scatter)
st.plotly_chart(fig)



locations = venue_locations(venues)
st.map(pd.DataFrame(locations))
