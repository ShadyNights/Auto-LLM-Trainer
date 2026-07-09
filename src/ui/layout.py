import streamlit as st
from typing import Optional

def get_layout_css() -> str:
    return """
    /* =========================================================================
       3. LAYOUT SYSTEM
       ========================================================================= */
    [data-testid="stSidebar"] {
        background-color: var(--c-layer-lowest) !important;
        border-right: 1px solid var(--c-outline-variant) !important;
    }
    """

def render_header(title: str, subtitle: Optional[str] = None, icon: Optional[str] = None):
    """Renders a page or section header (Maps to Headline 2 or 3)."""
    icon_html = f"<span aria-hidden='true' style='margin-right:8px;'>{icon}</span>" if icon else ""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    
    st.markdown(f"""
    <div style="margin-bottom: var(--space-lg);">
        <h2>{icon_html}{title}</h2>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)

def render_section(title: str, subtitle: Optional[str] = None, icon: Optional[str] = None):
    """Renders a standardized section layout."""
    icon_html = f"<span aria-hidden='true' style='margin-right:8px;'>{icon}</span>" if icon else ""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f"<div style='margin-bottom: var(--space-md);'><h3>{icon_html}{title}</h3>{subtitle_html}</div>", unsafe_allow_html=True)
