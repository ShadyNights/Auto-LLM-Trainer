from .styles import get_global_css
import streamlit as st

def inject_styles():
    """Injects the global CSS design system into the Streamlit app."""
    st.markdown(get_global_css(), unsafe_allow_html=True)
