# Standard imports
import pandas as pd

# matplotlib
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#import seaborn as sns

#plotly
import plotly.express as px
import plotly.graph_objects as go

#streamlit
import streamlit as st
from streamlit_option_menu import option_menu as om

#others
from copy import deepcopy
import json

st.header("Migros Stores Consultancy in Switzerland")

with st.sidebar:
    selected = om(
        'Navigation',
        ['Google Map', 'Open Street Map', 'Data Processing', 'Settings'],
        icons=['house', 'pin-map', 'cloud-download', 'gear'],
        menu_icon='',
        default_index=0,
        orientation='vertical'
    )

if selected == 'Google Map':
    exec(open('./src/Page/GoogleMapPage.py').read())
elif selected == 'Open Street Map':
    exec(open('./src/Page/OpenStreetMapPage.py').read())
elif selected == 'Data Processing':
    exec(open('./src/Page/DataProcessingPage.py').read())
else:
    st.write('Settings Page - TODO')