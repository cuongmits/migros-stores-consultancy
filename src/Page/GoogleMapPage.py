import streamlit as st
import plotly.express as px
from copy import deepcopy

# Reading data
@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

df_raw = load_data(path='./data/processed/supermarkets_new.csv')
df = deepcopy(df_raw)
with open("./data/raw/georef-switzerland-kanton.geojson") as response:
    geo_df_raw = json.load(response)

### Processing data
# TODO: Remove duplications by uniqueID

# Number of Migros stores per city
reduced_df = df.groupby(by=['commune', 'is_migros']).size().reset_index(name='count')
# store_count_df = reduced_df.set_index(['commune', 'is_migros'])['count'].unstack()
# store_count_df = store_count_df.rename(columns={True: 'is_migros', False: 'is_competitor'})
# store_count_df['is_migros'] = store_count_df['is_migros'].fillna(0).astype('int')
# store_count_df['is_competitor'] = store_count_df['is_competitor'].fillna(0).astype('int')
# store_count_df['total'] = store_count_df['is_migros'] + store_count_df['is_competitor']
# st.dataframe(data=store_count_df)

st.subheader("Plotting")

## Mapping Commune to Canton

# Get Caton Dictionary
canton_dict = {}
data = json.load(open("./data/raw/gemeinden-json.json"))
for item in data:
    canton_dict[item['gemeinde']['NAME']] = item['kanton']['NAME']

# Add Canton column
mapped_reduced_df = reduced_df.copy()
mapped_reduced_df['canton'] = mapped_reduced_df['commune'].map(canton_dict)

# Number of Migros stores per Canton
mapped_reduced_df = mapped_reduced_df.groupby(by=['canton', 'is_migros']).agg({
    'count': 'sum'
}).reset_index()

store_count_df = mapped_reduced_df.set_index(['canton', 'is_migros'])['count'].unstack().reset_index()
store_count_df = store_count_df.rename(columns={True: 'is_migros', False: 'is_competitor'})
store_count_df['is_migros'] = store_count_df['is_migros'].fillna(0).astype('int')
store_count_df['is_competitor'] = store_count_df['is_competitor'].fillna(0).astype('int')
store_count_df['total'] = store_count_df['is_migros'] + store_count_df['is_competitor']
mapped_reduced_df = store_count_df

# Add population & some indicators to choose places to open new stores
canton_population = pd.read_csv("./data/processed/canton_population.csv", low_memory=False)
mapped_reduced_df = mapped_reduced_df.join(canton_population.set_index('canton'), on='canton')
mapped_reduced_df['popul_per_store'] = mapped_reduced_df['population'] / mapped_reduced_df['total']
mapped_reduced_df['market_percent'] = mapped_reduced_df['is_migros'] * 100 / mapped_reduced_df['total']
    
## Plot against Canton
st.text('Population per store density')
fig = px.choropleth_mapbox(
    mapped_reduced_df,
    geojson=geo_df_raw,
    color="popul_per_store",
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
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)

## Plot against Canton
st.text('Market Percent per Canton')
fig2 = px.choropleth_mapbox(
    mapped_reduced_df,
    geojson=geo_df_raw,
    color="market_percent",
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
    st.text('All Store Brand Data in Switzerland')
    st.dataframe(data=df)
    st.text('Store data regarding communes')
    st.dataframe(data=reduced_df)
    st.text('Store data regarding cantons')
    st.dataframe(data=mapped_reduced_df)