import streamlit as st

from .animations import get_animations_css
from .components import get_components_css
from .layout import get_layout_css
from .theme import get_theme_css
from .tokens import get_tokens_css


def inject_styles():
    """Assembles all CSS and injects it into the page."""
    css = "\\n".join([get_tokens_css(), get_theme_css(), get_layout_css(), get_components_css(), get_animations_css()])
    fonts = (
        '<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Space+Grotesk:wght@700&family=JetBrains+Mono&display=swap" rel="stylesheet">'
        '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">'
    )
    st.markdown(fonts, unsafe_allow_html=True)
    st.markdown(f"<style>\n{css}\n</style>", unsafe_allow_html=True)
