import textwrap

import streamlit as st


def render_empty_state(title: str, description: str, icon: str = "info", action_label: str = None) -> None:
    """Renders a beautiful empty state indicator."""
    html = f"""
    <div class="c-empty-state">
        <span class="material-symbols-outlined">{icon}</span>
        <h4>{title}</h4>
        <p>{description}</p>
    </div>
    """
    st.markdown(textwrap.dedent(html).replace("\n", ""), unsafe_allow_html=True)
    if action_label:
        st.button(action_label, use_container_width=True)
