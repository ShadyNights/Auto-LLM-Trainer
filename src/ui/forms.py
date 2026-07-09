import streamlit as st
from typing import List, Tuple
from .layout import render_section

def render_travel_form() -> Tuple[str, int, str, str, bool]:
    """
    Renders the main travel configuration form.
    Returns: (city, days, interests, budget, is_submitted)
    """
    render_section("Configure Request", "Set the parameters for your next adventure.")
    
    with st.form("travel_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            city = st.text_input("Destination City", max_chars=50, placeholder="e.g. Kyoto, Japan")
            days = st.number_input("Travel Duration (Days)", min_value=1, max_value=14, value=5)
        with col_b:
            interests = st.text_input("Core Interests", placeholder="e.g. History, Food, Hiking")
            budget = st.selectbox("Budget Profile", ["Budget", "Moderate", "Luxury"])
            
        st.markdown("<hr style='margin-top:8px;'/>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Generate Premium Itinerary")
        
    return city, days, interests, budget, submitted
