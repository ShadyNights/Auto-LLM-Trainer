import streamlit as st
from typing import List, Optional
from .layout import render_section
from .components import render_badge
from .metrics import render_kpi_dashboard
from .helpers import render_divider

def render_sidebar(
    session_id: str, 
    warnings: List[str], 
    config_active: bool,
    metrics_data: Optional[dict]
):
    """Renders the persistent sidebar navigation and contextual panels."""
    with st.sidebar:
        # 1. Workspace
        render_section("Workspace", icon="🛠️")
        st.markdown(f"<p style='color:var(--c-secondary); margin:0;'>Session ID</p>", unsafe_allow_html=True)
        st.markdown(f"<code style='color:var(--c-primary);'>{session_id}</code>", unsafe_allow_html=True)
        render_divider()
        
        # 2. Health
        render_section("System Health", icon="⚙️")
        if warnings:
            st.markdown(render_badge("Degraded", "error"), unsafe_allow_html=True)
            for w in warnings:
                st.caption(f"⚠️ {w}")
        else:
            st.markdown(render_badge("Operational", "primary"), unsafe_allow_html=True)
        render_divider()
            
        # 3. Configuration
        render_section("Configuration", icon="🧠")
        if config_active:
            st.markdown(f"<p style='color:var(--c-secondary); margin:0;'>Provider: <b>Groq</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:var(--c-secondary); margin:0;'>Prompt: <b>v1</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:var(--c-secondary); margin:0;'>Dataset: <b>ds-v1</b></p>", unsafe_allow_html=True)
        else:
            st.markdown(render_badge("Config Error", "error"), unsafe_allow_html=True)
        render_divider()

        # 4. Metrics
        render_section("Metrics", icon="📊")
        render_kpi_dashboard(metrics_data)
