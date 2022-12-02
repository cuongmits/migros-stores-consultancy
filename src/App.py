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
        ['Store Location', 'Microeconomic Criterias', 'Macroeconomic Criterias', 'Supermarket Density', 'Datasets', 'About Us', 'Open Street Map', 'Data Processing', 'Settings'],
        icons=['pin-map', 'map', 'people', 'eye', 'clipboard-data', 'bookmark-star', 'pin-map', 'cloud-download', 'gear'],
        menu_icon='',
        default_index=0,
        orientation='vertical'
    )

if selected == 'Store Location':
    exec(open('./src/Page/StoreLocationPage.py').read())
elif selected == 'Microeconomic Criterias':
    exec(open('./src/Page/MicroeconomicCriteriasPage.py').read())
elif selected == 'Macroeconomic Criterias':
    exec(open('./src/Page/MacroeconomicCriteriasPage.py').read())
elif selected == 'Supermarket Density':
    exec(open('./src/Page/CompetitorsPage.py').read())
elif selected == 'Datasets':
    exec(open('./src/Page/DatasetsPage.py').read())
elif selected == 'About Us':
    exec(open('./src/Page/AboutUsPage.py').read())
elif selected == 'Open Street Map':
    exec(open('./src/Page/OpenStreetMapPage.py').read())
elif selected == 'Data Processing':
    exec(open('./src/Page/DataProcessingPage.py').read())
else:
    st.write('Settings Page - TODO')