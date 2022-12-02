import streamlit as st
from pathlib import Path

st.markdown(
    Path('./README.md').read_text(),
    unsafe_allow_html=True
)