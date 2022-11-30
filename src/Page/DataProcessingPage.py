import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.write('This map explains how we get the complete data of Migros Stores from the whole Switzerland')

data = {
    'Name':['Point #0', 'Point #1','Point #2','Point #3', 'Point #4', 'Point #5', 'Point #6', 'Point #7'],
    'lat':[46.523178, 46.941743, 47.355897, 47.021578, 46.702594, 46.485156, 46.320559, 46.779742],
    'lon':[6.667361, 7.439682, 8.493598, 9.192196, 9.744721, 8.880970, 7.680142, 8.411049],
    'Range': np.ones(8) * 350 # ~ 100km / distance from Bern to Zurich
}

plane_df = pd.DataFrame(data)

token = "pk.eyJ1IjoiYXRoYXJ2YWthdHJlIiwiYSI6ImNrZ2dkNHQ5MzB2bDUyc2tmZWc2dGx1eXQifQ.lVdNfajC6maADBHqsVrpcg"

fig = go.Figure(go.Scattermapbox(
    mode = "markers+text",
    lon = plane_df['lon'], lat = plane_df['lat'],
    marker = {'size': 20, 'symbol': "circle", 'allowoverlap': False,},
    hoverinfo='none',
    text = plane_df['Name'],
    textposition = "bottom right",
    textfont={'size':20, 'color':'blue'}
))

fig.add_trace(go.Scattermapbox(
    mode = "markers",
    lon = plane_df['lon'], lat = plane_df['lat'],
    marker = {'size': plane_df['Range']*50, 'sizemode':'area', 'symbol': "circle", 'opacity':0.3, 'allowoverlap': True,},
    hoverinfo='skip',
    text = plane_df['Name'],textposition = "bottom right"))

fig.update_layout(
    mapbox = {
        'accesstoken': token,
        'style': "streets",
        'bearing': 0,
        'pitch': 0,
        'center':{"lat": 46.8, "lon": 8.3},
        'zoom': 6
    },
    showlegend = False)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig)