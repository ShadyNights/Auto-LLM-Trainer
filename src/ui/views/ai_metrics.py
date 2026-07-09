import streamlit as st
from src.repositories.metrics_repository import MetricsRepository
from src.ui.components.cards.metric_card import render_metric_card

def render_ai_metrics_view(repo: MetricsRepository):
    st.markdown("<h2>AI Metrics</h2>", unsafe_allow_html=True)
    st.caption("Real-time telemetry and pipeline health.")
    
    metrics = repo.get_ai_metrics()
    
    st.markdown("### Usage")
    c1, c2, c3, c4 = st.columns(4)
    with c1: render_metric_card("Conversations", str(metrics.total_conversations), "forum")
    with c2: render_metric_card("Generated", str(metrics.successful_generations), "check_circle")
    with c3: render_metric_card("Failures", str(metrics.failed_generations), "error")
    with c4: render_metric_card("Success Rate", f"{metrics.success_rate:.1f}%", "percent")
    
    st.markdown("### Quality & Performance")
    c1, c2, c3, c4 = st.columns(4)
    with c1: render_metric_card("Avg Rating", f"{metrics.average_rating:.1f}⭐" if metrics.average_rating else "N/A", "star")
    with c2: render_metric_card("Quality Score", f"{metrics.average_quality_score:.1f}" if metrics.average_quality_score else "N/A", "analytics")
    with c3: render_metric_card("Gen Time", f"{metrics.average_generation_time_ms:.0f} ms", "timer")
    with c4: render_metric_card("Provider Latency", f"{metrics.provider_latency:.0f} ms", "speed")
    
    st.markdown("### Pipeline Health")
    c1, c2, c3 = st.columns(3)
    with c1: render_metric_card("Learning Queue", str(metrics.learning_queue_size), "pending")
    with c2: render_metric_card("Dead Queue", str(metrics.dead_letter_queue_size), "delete")
    with c3: render_metric_card("Evaluations", str(metrics.evaluations), "rule")
