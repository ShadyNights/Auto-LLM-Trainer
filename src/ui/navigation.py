import streamlit as st

from .components import render_badge
from .helpers import render_divider
from .layout import render_section


def render_sidebar(session_id: str, warnings: list[str], config_active: bool):
    """Renders the persistent sidebar navigation and contextual panels."""
    with st.sidebar:
        # 0. Navigation Routing
        render_section("Navigation", icon="explore")
        pages = ["Generator", "Trip Summary", "AI Metrics", "Analytics Dashboard", "Database Manager"]
        current_page = st.radio("Pages", pages, label_visibility="collapsed")
        render_divider()

        # 1. Workspace
        render_section("Workspace", icon="build_circle")
        st.markdown("<p class='c-meta-label'>Session ID</p>", unsafe_allow_html=True)
        session_display = session_id if session_id else "New Session"
        st.markdown(f"<code class='c-meta-value'>{session_display}</code>", unsafe_allow_html=True)
        render_divider()

        # 2. Health
        render_section("System Health", icon="monitor_heart")
        if warnings:
            st.markdown(render_badge("Degraded", "error"), unsafe_allow_html=True)
            for w in warnings:
                st.caption(f"⚠️ {w}")
        else:
            st.markdown(render_badge("Operational", "primary"), unsafe_allow_html=True)
        render_divider()

        # 3. Configuration
        render_section("Configuration", icon="memory")
        if config_active:
            st.markdown(
                "<p class='c-meta-label'>Prompt: <span class='c-meta-value'>v1</span></p>", unsafe_allow_html=True
            )
            st.markdown(
                "<p class='c-meta-label'>Dataset: <span class='c-meta-value'>ds-v1</span></p>", unsafe_allow_html=True
            )
        else:
            st.markdown(render_badge("Config Error", "error"), unsafe_allow_html=True)

        return current_page
