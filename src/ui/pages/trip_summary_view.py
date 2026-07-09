import streamlit as st
from ..layout import render_header
from ..components import render_empty_state, render_card

def render_trip_summary():
    render_header("Trip Summary", "Details for your active adventure request.", "map")
    
    if "trip_params" not in st.session_state:
        render_empty_state("No Active Trip", "Generate a trip first to see the summary.", "explore")
        return
        
    params = st.session_state.trip_params
    interests = ', '.join(params['interests']) if params['interests'] else 'None specified'
    
    html = f'<div class="l-stack"><div><p class="c-meta-label">Destination</p><p class="c-meta-value">{params["city"]}</p></div><div><p class="c-meta-label">Duration</p><p class="c-meta-value">{params["days"]} days</p></div><div><p class="c-meta-label">Budget</p><p class="c-meta-value">{params["budget"]}</p></div><div><p class="c-meta-label">Core Interests</p><p class="c-meta-value">{interests}</p></div></div>'
    render_card(html)
