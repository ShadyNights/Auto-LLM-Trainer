from .tokens import get_tokens_css
from .base import get_base_css
from .layout import get_layout_css
from .components import get_components_css
from .animations import get_animations_css
from .utilities import get_utilities_css
import streamlit as st

def get_global_css() -> str:
    """Aggregates all CSS modules into a single stylesheet."""
    css = "\\n".join([
        get_tokens_css(),
        get_base_css(),
        get_layout_css(),
        get_components_css(),
        get_animations_css(),
        get_utilities_css()
    ])
    return f"<style>\\n{css}\\n</style>"

def inject_styles():
    """Injects the global CSS design system into the Streamlit app."""
    st.markdown(get_global_css(), unsafe_allow_html=True)
