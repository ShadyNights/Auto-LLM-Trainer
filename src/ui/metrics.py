import streamlit as st
from .components import render_metric

def render_kpi_dashboard(metrics_data: dict):
    """Renders a collection of metrics for the dashboard."""
    if not metrics_data:
        render_metric("Metrics", "Offline", "DB Error", "error")
        return
        
    total_convos = metrics_data.get('total_conversations', 0)
    render_metric("Total Conversations", str(total_convos), icon="forum", context="Across all users.")
    st.markdown("<br/>", unsafe_allow_html=True)
    
    rating = metrics_data.get('average_rating', 0)
    rating_str = f"{rating:.1f}" if rating else "N/A"
    render_metric("Avg Rating", rating_str, icon="star", trend_label="Stable", variant="neutral", context="Based on user feedback.")
    st.markdown("<br/>", unsafe_allow_html=True)
    
    fails = metrics_data.get('generation_failures', 0)
    fail_trend = "Needs Review" if fails > 0 else "Optimal"
    fail_color = "error" if fails > 0 else "primary"
    render_metric("Gen Failures", str(fails), icon="warning", trend_label=fail_trend, variant=fail_color, context="Pipeline failure count.")
