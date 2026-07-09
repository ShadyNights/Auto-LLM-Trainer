import streamlit as st
from src.repositories.trip_repository import TripRepository
from src.ui.state.dashboard_state import DashboardState
from src.ui.components.empty_state import render_empty_state
from src.ui.components.cards.metric_card import render_metric_card
from src.ui.components.badges import render_badge

def render_trip_summary_view(repo: TripRepository):
    st.markdown("<h2>Trip Summary</h2>", unsafe_allow_html=True)
    st.caption("Detailed overview of your active itinerary.")
    
    active_id = DashboardState.get_active_itinerary_id()
    if not active_id:
        render_empty_state(
            title="No Active Trip",
            description="Generate a trip from the dashboard first to see the summary.",
            icon="explore"
        )
        return
        
    summary = repo.get_trip_summary(active_id)
    if not summary:
        render_empty_state("Trip Not Found", "The requested itinerary could not be loaded.", "error")
        return
        
    # Hero Summary
    st.markdown(f"### {summary.destination}")
    st.markdown(f"**{summary.duration} Days** • **{summary.budget} Budget**")
    
    # Quick Stats
    c1, c2, c3, c4 = st.columns(4)
    with c1: render_metric_card("Complexity", f"{summary.trip_complexity} pts", "timeline")
    with c2: render_metric_card("Quality Score", f"{summary.quality_score or 0.0:.1f}", "analytics")
    with c3: render_metric_card("Gen Time", f"{summary.generation_time_ms or 0} ms", "timer")
    with c4: render_metric_card("Conversation", f"#{summary.conversation_id}", "forum")
    
    st.markdown("---")
    
    # Travel Details
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Travel Details")
        st.write(f"**Styles:** {', '.join(summary.travel_style) if summary.travel_style else 'None'}")
        st.write(f"**Interests:** {', '.join(summary.interests) if summary.interests else 'None'}")
        
    with c2:
        st.markdown("#### AI Insights")
        st.write(f"**Provider:** {summary.provider}")
        st.write(f"**Model:** {summary.model_version}")
        st.write(f"**Prompt:** {summary.prompt_version}")
        st.write(f"**Created:** {summary.created_at.strftime('%Y-%m-%d %H:%M')}")
        
    st.markdown("---")
    st.markdown("#### Quick Actions")
    col1, col2, col3 = st.columns([1,1,2])
    with col1: st.button("Export PDF", use_container_width=True)
    with col2: st.button("Share Link", use_container_width=True)
