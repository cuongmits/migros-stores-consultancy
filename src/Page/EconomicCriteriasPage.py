import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import numpy as np
from plotly.subplots import make_subplots
import json
import geojson

import streamlit as st


# # Reading data
# @st.cache
# def load_data(path):
#     df = pd.read_csv(path)
#     return df

# df_raw = load_data(path='./data/processed/migros_stores_data.csv')
# df = deepcopy(df_raw)

### Step 1

bip_kanton = pd.read_csv('./data/git/BIP_Kanton_2019.csv')
population_df = pd.read_csv('./data/git/df_population_cleaned_final.csv')
income_zürich_df = pd.read_csv('./data/git/income_zurich_2021.csv')
# Open the Geojson, and change the key for the maps - BFS number, works not with a point
with open("./data/git/gemeinden-geojson.geojson") as f:
    gj = geojson.load(f)

for i in range(len(gj["features"])):
    gj["features"][i]['properties']['gemeinde_BFS_NUMMER'] = gj["features"][i]['properties'].pop('gemeinde.BFS_NUMMER')

### Step 2

#Population density in Switzerland per Commune, use the csv df_population_cleaned_final.csv
#we decided not to show

#Change of the population in the Communes in percent, use the csv df_population_cleaned_final.csv
st.subheader(">>>> Title for this?")
fig_pop_change = go.Figure(
    go.Choroplethmapbox(
        geojson=gj,
        locations=population_df.Number_of_commune,
        z=population_df.Population_change_perc,
        colorscale="Viridis",
        featureidkey="properties.gemeinde_BFS_NUMMER",
        zmin = -20,
        zmax = 30,
        marker_opacity=0.5,
        marker_line_width=0
    )
)
fig_pop_change.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=6,
    mapbox_center={"lat": 46.8200, "lon": 8.4070})
fig_pop_change.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_pop_change)

### Step 3

# Show the average income for the Kanton of Zürich, use the csv income_zürich_2021.csv
st.subheader("Everage Income for Kanton of Zürich")
fig_inc = go.Figure(
    go.Choroplethmapbox(
        geojson=gj, locations=income_zürich_df.BFS_NR, z=income_zürich_df.INDIKATOR_VALUE,
        colorscale="Viridis",featureidkey="properties.gemeinde_BFS_NUMMER",
        zmin = 60000 , zmax = 100000, marker_opacity=0.5, marker_line_width=0
    )
)
fig_inc.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=8, mapbox_center = {"lat": 47.3769, "lon": 8.5417})
fig_inc.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_inc)

### Step 4

# GDP per Kantone, use the csv BIP_Kanton_2019.csv
st.subheader("GDP per Kantone")
bip_kanton = bip_kanton.sort_values(by='GDP_2019',ascending=False)
fig_gdp = px.bar(
    bip_kanton, x='Kanton_name', y='GDP_2019',
    labels={"Kanton_name": "Name of the Kantones","GDP_2019": "GDP in millions (CHF)"})
fig_gdp.update_layout(title = 'GDP in millions (CFH) per Kanton in 2019', title_x=0.5)
st.plotly_chart(fig_gdp)