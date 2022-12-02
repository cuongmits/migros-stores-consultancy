import pandas as pd
import plotly.graph_objects as go
import json
import geojson

import streamlit as st

# Open the Geojson, and change the key for the maps - BFS number, works not with a point
with open("./data/git/gemeinden-geojson.geojson") as f:
    gj = geojson.load(f)

for i in range(len(gj["features"])):
    gj["features"][i]['properties']['gemeinde_BFS_NUMMER'] = gj["features"][i]['properties'].pop('gemeinde.BFS_NUMMER')


### Step 1

merged_df_only_relevant_big_supermarkets = pd.read_csv("./data/git/merged_df_only_relevant_big_supermarkets.csv")

### Step 2

# showing only the N of Supermarkets per 1000 residents
st.subheader("Numer of Supermarkets per 1000 residents")
fig = go.Figure(go.Choroplethmapbox(
    geojson=gj,
    locations=merged_df_only_relevant_big_supermarkets.Number_of_commune,
    z=merged_df_only_relevant_big_supermarkets.N_markets_per_1k_residents,
    colorscale="RdBu", featureidkey="properties.gemeinde_BFS_NUMMER",
    #text=pop_clean['text'],
    zmin = 0 , zmax = 10, marker_opacity=0.5, marker_line_width=0))
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=6, mapbox_center = {"lat": 46.8200, "lon": 8.4070})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)

### Step 3

st.subheader("Big chain only Supermarkets per 1000 residents")
fig = go.Figure(go.Choroplethmapbox(
    geojson=gj, locations=merged_df_only_relevant_big_supermarkets.Number_of_commune, z=merged_df_only_relevant_big_supermarkets.N_big_markets_per_1k_residents,
    colorscale="Viridis", featureidkey="properties.gemeinde_BFS_NUMMER",
    #text=pop_clean['text'],
    zmin=0, zmax=1, marker_opacity=0.5, marker_line_width=0))     
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=6, mapbox_center = {"lat": 46.8200, "lon": 8.4070})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)
