from typing import Optional
import streamlit as st
from .layout import render_header, render_section
from .components import render_loading
from .cards import render_itinerary_card, render_analytics_card, render_feedback_form
from .helpers import render_spacer
from .metrics import render_kpi_dashboard

def render_hero_dashboard(metrics_data: Optional[dict]):
    """Renders the main hero area and the horizontal KPI dashboard."""
    render_header(
        title="Traveler LLM", 
        subtitle="Automated itinerary curation powered by a Continuous Feedback Learning Pipeline.",
        icon="flight_takeoff"
    )
    
    # Render KPI metrics horizontally below the header
    render_spacer(1)
    if metrics_data:
        col1, col2, col3 = st.columns(3)
        
        total_convos = metrics_data.get('total_conversations', 0)
        with col1:
            from .components import render_metric
            render_metric("Total Conversations", str(total_convos), icon="forum", context="Across all users.")
            
        with col2:
            rating = metrics_data.get('average_rating', 0)
            rating_str = f"{rating:.1f}" if rating else "N/A"
            render_metric("Avg Rating", rating_str, icon="star", trend_label="Stable", variant="neutral", context="Based on user feedback.")
            
        with col3:
            fails = metrics_data.get('generation_failures', 0)
            fail_trend = "Needs Review" if fails > 0 else "Optimal"
            fail_color = "error" if fails > 0 else "primary"
            render_metric("Gen Failures", str(fails), icon="warning", trend_label=fail_trend, variant=fail_color, context="Pipeline failure count.")
            
    render_spacer(1)

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
    
    tab1, tab2, tab3 = st.tabs(["Itinerary", "Analytics", "Feedback"])
    
    with tab1:
        render_itinerary_card(itinerary_text)
        
    with tab2:
        render_analytics_card(itinerary_id, corr_id)
        
    with tab3:
        return render_feedback_form()
        
    return None, None, False
