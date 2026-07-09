import streamlit as st
from typing import List, Optional
from .layout import render_section
from .components import render_badge
from .metrics import render_kpi_dashboard
from .helpers import render_divider

def render_sidebar(
    session_id: str, 
    warnings: List[str], 
    config_active: bool
):
    """Renders the persistent sidebar navigation and contextual panels."""
    with st.sidebar:
        # 0. Navigation Routing
        render_section("Navigation", icon="explore")
        pages = ["Generator", "Trip Summary", "AI Metrics", "Analytics Dashboard", "Database Manager"]
        current_page = st.radio("Pages", pages, label_visibility="collapsed")
        render_divider()

        # 1. Workspace
        render_section("Workspace", icon="🛠️")
        st.markdown(f"<p class='c-meta-label'>Session ID</p>", unsafe_allow_html=True)
        st.markdown(f"<code class='c-meta-value'>{session_id}</code>", unsafe_allow_html=True)
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
            st.markdown(f"<p class='c-meta-label'>Provider: <span class='c-meta-value'>Groq</span></p>", unsafe_allow_html=True)
            st.markdown(f"<p class='c-meta-label'>Prompt: <span class='c-meta-value'>v1</span></p>", unsafe_allow_html=True)
            st.markdown(f"<p class='c-meta-label'>Dataset: <span class='c-meta-value'>ds-v1</span></p>", unsafe_allow_html=True)
        else:
            st.markdown(render_badge("Config Error", "error"), unsafe_allow_html=True)
            
        return current_page

