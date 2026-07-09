"""
Layout primitives defining standard container boundaries.
"""
import streamlit as st

def container_main():
    """Sets the max-width and center alignment for the main application container."""
    st.markdown("""
    <style>
        .block-container {
            max-width: 1024px;
            padding-top: var(--space-8);
            padding-bottom: var(--space-16);
        }
    </style>
    """, unsafe_allow_html=True)
