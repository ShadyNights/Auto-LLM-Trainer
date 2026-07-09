import streamlit as st
from src.repositories.analytics_repository import AnalyticsRepository
from ..layout import render_header, render_section

def render_database_manager(repo: AnalyticsRepository):
    render_header("Database Manager", "Direct view of generated trips and records.", "database")
    
    records = repo.get_recent_records(limit=100)
    
    render_section(f"Total Records: {len(records)}", icon="list")
    
    if not records:
        st.caption("No records found in database.")
        return
        
    for r in records:
        # Example format: #17 • Russia — 1d (Moderate)
        dest = r['destination']
        dur = r['duration']
        bud = r['budget_level']
        item_id = r['itinerary_id']
        st.markdown(f"**#{item_id}** • {dest} — {dur}d ({bud})")
