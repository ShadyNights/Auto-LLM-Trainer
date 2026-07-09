import textwrap

import streamlit as st


def render_metric_card(title: str, value: str, icon: str = None, context: str = None) -> None:
    icon_html = f"<span class='material-symbols-outlined'>{icon}</span>" if icon else ""
    ctx_html = f"<div class='c-metric-card__context'>{context}</div>" if context else ""

    html = f"""
    <div class="c-metric-card">
        <div class="c-metric-card__header">
            {icon_html}
            <span>{title}</span>
        </div>
        <div class="c-metric-card__value">{value}</div>
        {ctx_html}
    </div>
    """
    st.markdown(textwrap.dedent(html).replace("\n", ""), unsafe_allow_html=True)
