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

### Processing data
# TODO: Remove duplications by uniqueID

# Number of Migros stores per city
reduced_df = df.groupby(by=['addr:city']).size().reset_index(name='count')

st.subheader("Plotting")

## Plot against cities (not Cantons)
st.text('Migros stores per city density')
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

## Mapping small city to City/Stadt

# Get Caton Dictionary
canton_dict = {}
data = json.load(open("./data/raw/gemeinden-json.json"))
for item in data:
    canton_dict[item['gemeinde']['NAME']] = item['kanton']['NAME']

# Add Canton column
mapped_reduced_df = reduced_df.copy()
mapped_reduced_df['canton'] = mapped_reduced_df['addr:city'].map(canton_dict)

# Number of Migros stores per Canton
mapped_reduced_df = mapped_reduced_df.groupby(by=['canton']).agg({
    'count': 'sum'
}).reset_index()
    
## Plot against Canton
st.text('Migros stores per Canton (after mapping) density')
fig2 = px.choropleth_mapbox(
    mapped_reduced_df,
    geojson=geo_df_raw,
    color="count",
    locations="canton",
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
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig2)

# Showing DataSet
if st.checkbox("Show DataFrame", value=False):
    st.subheader("Dataset")
    st.text('Migros Stores Data in Switzerland')
    st.dataframe(data=df)
    st.text('Processed Data')
    st.text('Problem: some cities don\'t have any canton')
    st.dataframe(data=reduced_df)
    st.text('Processed Data')
    st.text('Problem: some cities don\'t have any canton')
    st.dataframe(data=mapped_reduced_df)