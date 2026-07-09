import streamlit as st
from src.repositories.analytics_repository import AnalyticsRepository
from ..layout import render_header, render_section
from ..components import render_metric

def render_analytics_dashboard(repo: AnalyticsRepository):
    render_header("Analytics Dashboard", "System-wide usage and popularity metrics.", "analytics")
    
    metrics = repo.get_ai_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric("Total Generated", str(metrics['data_points']), icon="description")
    with col2:
        render_metric("Training Cycles", str(metrics['training_cycles']), icon="model_training")
    with col3:
        avg = f"{metrics['average_rating']:.1f}" if metrics['average_rating'] > 0 else "N/A"
        render_metric("Avg Rating", f"{avg}⭐", icon="star")
    with col4:
        # Just to have 4 metrics, we can add something else or leave empty.
        pass
        
    st.markdown("<br/>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        render_section("Popular Destinations", icon="public")
        destinations = repo.get_popular_destinations(limit=10)
        if destinations:
            # Format as requested: "Thailand — 3 itineraries"
            for d in destinations:
                st.markdown(f"**{d['destination']}** — {d['trip_count']} itineraries")
        else:
            st.caption("No data available yet.")
            
    with c2:
        render_section("⭐ Rating Distribution", icon="bar_chart")
        distribution = repo.get_rating_distribution()
        if distribution:
            for d in distribution:
                stars = "⭐" * int(d['rating'])
                st.markdown(f"**{stars}** — {d['count']} itineraries")
        else:
            st.caption("No ratings available yet.")
