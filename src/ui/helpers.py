import re
import streamlit as st

def sanitize_text(text: str, max_length: int = 50) -> str:
    """Sanitizes basic text input by removing special characters."""
    if not text:
        return ""
    return re.sub(r'[^a-zA-Z\s-]', '', str(text).strip())[:max_length]

def render_spacer(height: int = 1):
    """Renders a vertical spacer."""
    for _ in range(height):
        st.markdown("<br/>", unsafe_allow_html=True)

def render_divider():
    """Renders a horizontal rule."""
    st.markdown("<hr/>", unsafe_allow_html=True)
