import streamlit as st
from .tokens import get_tokens_css
from .theme import get_theme_css
from .layout import get_layout_css
from .components import get_components_css
from .animations import get_animations_css

def inject_styles():
    """Assembles all CSS and injects it into the page."""
    css = "\\n".join([
        get_tokens_css(),
        get_theme_css(),
        get_layout_css(),
        get_components_css(),
        get_animations_css()
    ])
    st.markdown(f"<style>\\n{css}\\n</style>", unsafe_allow_html=True)
