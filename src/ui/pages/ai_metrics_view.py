import streamlit as st
from src.repositories.analytics_repository import AnalyticsRepository
from ..layout import render_header
from ..components import render_metric

def render_ai_metrics(repo: AnalyticsRepository):
    render_header("AI Metrics", "Telemetry and learning pipeline statistics.", "memory")
    
    metrics = repo.get_ai_metrics()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric("Data Points", str(metrics['data_points']), icon="dataset", context="Total generated samples.")
    with col2:
        render_metric("Training Cycles", str(metrics['training_cycles']), icon="model_training", context="Completed iterations.")
    with col3:
        avg = f"{metrics['average_rating']:.1f}" if metrics['average_rating'] > 0 else "N/A"
        render_metric("Average Rating", f"{avg}⭐", icon="star", context="User feedback average.")
