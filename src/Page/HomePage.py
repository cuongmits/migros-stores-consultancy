import streamlit as st
import plotly.express as px
from copy import deepcopy

# Reading data
@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

df_raw = load_data(path='./data/processed/migros_stores_data.csv')
df = deepcopy(df_raw)
with open("./data/raw/georef-switzerland-kanton.geojson") as response:
    geo_df_raw = json.load(response)

# Process data
reduced_df = df.groupby(by=['addr:city']).size().reset_index(name='count')

# Control Panel
if st.checkbox("Show DataFrame", value=False):
    st.subheader("Dataset")
    st.text('Migros Stores Data in Switzerland')
    st.dataframe(data=df)
    st.text('Processed Data')
    st.dataframe(data=reduced_df)

fig = px.choropleth_mapbox(
    reduced_df,
    geojson=geo_df_raw,
    color="count",
    locations="addr:city",
    featureidkey="properties.kan_name", #TODO: we should map regions/towns to city
    center={"lat": 46.8, "lon": 8.3},
    mapbox_style="carto-positron",
    opacity=0.8,
    width=800,
    height=600,
    hover_data=[],
    zoom=6,
    title='Migros Stores density in Switzerland', # <<< this doesn't make any changes!
)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)