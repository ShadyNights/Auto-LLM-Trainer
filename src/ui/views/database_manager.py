import streamlit as st
from src.repositories.database_repository import DatabaseRepository
from src.domain.enums.table_type import TableType
from src.ui.components.cards.metric_card import render_metric_card

@st.cache_data(ttl=30)
def fetch_table(_repo: DatabaseRepository, table: TableType):
    return _repo.get_records(table, limit=50)

def render_database_manager_view(repo: DatabaseRepository):
    st.markdown("<h2>Database Manager</h2>", unsafe_allow_html=True)
    st.caption("Direct administration view of the PostgreSQL database.")
    
    # 1. Summary Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1: render_metric_card("Itineraries", str(repo.get_record_count(TableType.ITINERARIES)), "map")
    with c2: render_metric_card("Conversations", str(repo.get_record_count(TableType.CONVERSATIONS)), "forum")
    with c3: render_metric_card("Events", str(repo.get_record_count(TableType.EVENTS)), "bolt")
    with c4: render_metric_card("Audit Logs", str(repo.get_record_count(TableType.AUDIT_LOGS)), "security")
    
    st.markdown("---")
    
    # 2. 11 Tabs
    tabs = st.tabs([
        "Itineraries", "Conversations", "Events", "Datasets", 
        "Model Versions", "Prompt Versions", "Evaluations", 
        "Training Queue", "Audit Logs", "System Config", "Trips"
    ])
    
    table_map = [
        TableType.ITINERARIES, TableType.CONVERSATIONS, TableType.EVENTS, TableType.DATASETS,
        TableType.MODEL_VERSIONS, TableType.PROMPTS_METADATA, TableType.CONFIG_EVALUATIONS,
        TableType.TRAINING_QUEUE, TableType.AUDIT_LOGS, TableType.SYSTEM_CONFIG, TableType.TRIPS
    ]
    
    for idx, tab in enumerate(tabs):
        with tab:
            df = fetch_table(repo, table_map[idx])
            if df.empty:
                st.caption("No records found in this table.")
            else:
                st.dataframe(df, use_container_width=True, hide_index=True)
