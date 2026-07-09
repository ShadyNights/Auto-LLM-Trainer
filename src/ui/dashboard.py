import streamlit as st
from .layout import render_header, render_section
from .components import render_loading
from .cards import render_itinerary_card, render_analytics_card, render_feedback_form
from .helpers import render_spacer

def render_hero_dashboard():
    """Renders the main hero area of the dashboard."""
    render_header(
        title="Traveler LLM", 
        subtitle="Automated itinerary curation powered by a Continuous Feedback Learning Pipeline.",
        icon="✈️"
    )

def render_processing_state():
    """Renders the LLM generation loading state."""
    render_spacer(1)
    render_section("Generation in Progress", "The LLM is processing your request...")
    render_loading()

def render_results_dashboard(itinerary_text: str, itinerary_id: str, corr_id: str) -> tuple[Optional[int], Optional[str], bool]:
    """
    Renders the tabbed dashboard for generated results.
    Returns: Feedback form results (rating, comments, submit_flag)
    """
    render_spacer(1)
    render_section("Generated Results", "Your requested itinerary is ready.")
    
    tab1, tab2, tab3 = st.tabs(["📝 Itinerary", "⚙️ Analytics", "⭐ Feedback"])
    
    with tab1:
        render_itinerary_card(itinerary_text)
        
    with tab2:
        render_analytics_card(itinerary_id, corr_id)
        
    with tab3:
        return render_feedback_form()
        
    return None, None, False
