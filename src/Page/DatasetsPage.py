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

# Number of Migros stores per city
reduced_df = df.groupby(by=['commune', 'is_migros']).size().reset_index(name='count')

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

### Raw Datasets

st.subheader("Raw dataset")

st.text('from Google Map')
st.dataframe(data=df)

st.text('from Open Street Map')
st.dataframe(data=load_data(path='./data/processed/migros_stores_data.csv'))

st.text('Regional Portrats 2021')
st.dataframe(data=pd.read_csv('./data/raw/RegionalPortraits21.03.01.csv', sep=';'))

st.text('Income Zurich 2021')
st.dataframe(data=pd.read_csv('./data/git/income_zurich_2021.csv'))

### Processed Datasets

st.subheader("Processed dataset")

# st.text('Store data regarding communes')
# st.dataframe(data=reduced_df)
st.text('Processed Store data regarding Kantons')
st.dataframe(data=mapped_reduced_df)

st.text('Market Share')
st.dataframe(data=pd.read_csv('./data/git/supermarket_share.csv'))

### More

st.subheader('... many more')