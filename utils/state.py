import streamlit as st

def init_state(gdf):
    if "original" not in st.session_state:
        st.session_state.original = gdf
        st.session_state.filtered = gdf