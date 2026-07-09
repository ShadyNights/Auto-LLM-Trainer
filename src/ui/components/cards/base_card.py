import streamlit as st
import textwrap

def render_card(content_html: str, variant: str = "default") -> None:
    """Renders a standard surface card."""
    html = f"""
    <div class="c-card c-card--{variant}">
        {content_html}
    </div>
    """
    st.markdown(textwrap.dedent(html).replace('\n', ''), unsafe_allow_html=True)
