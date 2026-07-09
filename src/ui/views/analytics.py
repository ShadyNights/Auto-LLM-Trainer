import streamlit as st
import pandas as pd
from src.repositories.analytics_repository import AnalyticsRepository
from src.ui.components.cards.metric_card import render_metric_card

@st.cache_data(ttl=30)
def fetch_analytics(_repo: AnalyticsRepository):
    return _repo.get_analytics()

def render_analytics_view(repo: AnalyticsRepository):
    st.markdown("<h2>Analytics Dashboard</h2>", unsafe_allow_html=True)
    st.caption("System-wide operational insights.")
    
    analytics = fetch_analytics(repo)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Destinations", "Ratings", "Budgets"])
    
    with tab1:
        st.markdown("#### Last 30 Days")
        c1, c2 = st.columns(2)
        with c1: render_metric_card("Generations", str(analytics.recent_generations), "bolt")
        with c2: render_metric_card("Conversations", str(analytics.recent_conversations), "forum")
        
        st.markdown("#### Pipeline Growth")
        c1, c2, c3 = st.columns(3)
        with c1: render_metric_card("Datasets", str(analytics.pipeline.total_datasets), "dataset")
        with c2: render_metric_card("Prompts", str(analytics.pipeline.total_prompts), "code")
        with c3: render_metric_card("Models", str(analytics.pipeline.total_models), "psychology")
        
    with tab2:
        st.markdown("#### Popular Destinations")
        if analytics.destinations:
            df = pd.DataFrame([{'Destination': d.destination, 'Trips': d.count, 'Avg Rating': d.avg_rating} for d in analytics.destinations])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.caption("Not Available")
            
    with tab3:
        st.markdown("#### Rating Distribution")
        if analytics.ratings:
            df = pd.DataFrame([{'Rating': f"{r.rating}⭐", 'Count': r.count} for r in analytics.ratings])
            st.bar_chart(data=df.set_index('Rating'))
        else:
            st.caption("Not Available")
            
    with tab4:
        st.markdown("#### Budget Distribution")
        if analytics.budgets:
            df = pd.DataFrame([{'Budget': b.budget_level, 'Count': b.count} for b in analytics.budgets])
            st.bar_chart(data=df.set_index('Budget'))
        else:
            st.caption("Not Available")
