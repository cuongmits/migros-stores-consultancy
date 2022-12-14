import streamlit as st
import plotly.express as px
from copy import deepcopy

# Reading data
@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

df_raw = load_data(path='./data/git/supermarkets_last.csv')
df = deepcopy(df_raw)

st.subheader("Store Location of all Brands")
fig = px.scatter_mapbox(
    df,
    lat='geometry.location.lat',
    lon='geometry.location.lng',
    hover_name="name",
    opacity=0.8,
    width=800,
    height=600,
    zoom=6.3,
    labels={'store_name': 'Store Brand'},
    color= 'store_name')
fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=800)
st.plotly_chart(fig)

### another Pie chart

st.subheader("Supermarket Share")
sm_share=load_data(path='./data/git/supermarket_share.csv')
fig = px.pie(sm_share, values='no_of_sm', names='store_name')
st.plotly_chart(fig)