import streamlit as st
from typing import Optional
import textwrap

def get_layout_css() -> str:
    return """
    /* =========================================================================
       3. LAYOUT SYSTEM
       ========================================================================= */
    [data-testid="stSidebar"] {
        background-color: var(--c-layer-lowest) !important;
        border-right: 1px solid var(--c-outline-variant) !important;
    }
    
    /* Streamlit Main Container Top Padding Reduction */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .l-mb-md { margin-bottom: var(--space-md); }
    .l-mb-lg { margin-bottom: var(--space-lg); }
    .l-icon { margin-right: var(--space-sm); }
    """

def render_header(title: str, subtitle: Optional[str] = None, icon: Optional[str] = None):
    """Renders a page or section header (Maps to Headline 2 or 3)."""
    icon_html = f"<span aria-hidden='true' class='l-icon material-symbols-outlined' style='font-size: 24px; vertical-align: middle;'>{icon}</span>" if icon else ""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    
    html = f'<div class="l-mb-lg"><h2>{icon_html}{title}</h2>{subtitle_html}</div>'
    st.markdown(html, unsafe_allow_html=True)

def render_section(title: str, subtitle: Optional[str] = None, icon: Optional[str] = None):
    """Renders a standardized section layout."""
    icon_html = f"<span aria-hidden='true' class='l-icon material-symbols-outlined' style='font-size: 20px; vertical-align: middle;'>{icon}</span>" if icon else ""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f"<div class='l-mb-md'><h3>{icon_html}{title}</h3>{subtitle_html}</div>", unsafe_allow_html=True)
