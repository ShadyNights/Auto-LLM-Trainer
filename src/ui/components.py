import streamlit as st
from typing import Optional

# =========================================================================
# COMPONENT LIBRARY (Strict Baseline)
# =========================================================================

def render_card(content_html: str, active_glow: bool = False, class_name: str = ""):
    """Renders a standard card layout in Streamlit."""
    classes = ["c-card"]
    if active_glow: classes.append("c-card--active-glow")
    if class_name: classes.append(class_name)
    
    html = f'<div class="{" ".join(classes)}">{content_html}</div>'
    st.markdown(html, unsafe_allow_html=True)

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
    """Renders a standardized section wrapper (Maps to Headline 3)."""
    icon_html = f"<span aria-hidden='true' style='margin-right:8px;'>{icon}</span>" if icon else ""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    
    st.markdown(f"""
    <div style="margin-bottom: var(--space-md);">
        <h3>{icon_html}{title}</h3>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)

def render_badge(text: str, variant: str = "neutral", class_name: str = "") -> str:
    """
    Renders an inline badge. 
    Supported Variants (Baseline): primary, error, neutral
    """
    return f'<span class="c-badge c-badge--{variant} {class_name}">{text}</span>'

def render_status(text: str, state: str = "neutral"):
    """Renders a badge directly into Streamlit."""
    st.markdown(render_badge(text, variant=state), unsafe_allow_html=True)

def render_metric(title: str, value: str, label: Optional[str] = None, variant: str = "neutral"):
    """Renders a professional metric layout (Metric Card)."""
    label_html = render_badge(label, variant=variant) if label else ""
    
    html = f"""
    <div class="c-metric">
        <div class="c-metric__title">{title}</div>
        <div class="c-metric__value">{value}</div>
        {label_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_empty_state(title: str, description: str, icon: str = "block"):
    """Renders an empty state."""
    st.markdown(f"""
    <div class="c-empty-state">
        <span class="material-symbols-outlined" style="font-size:32px; color:var(--c-secondary); margin-bottom:var(--space-md);">{icon}</span>
        <h3>{title}</h3>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_loading(title: str = "Processing...", description: str = "Please wait", lines: int = 3):
    """Renders a skeleton loading state."""
    lines_html = "".join(['<div class="c-skeleton" style="height:16px; width:100%; margin-bottom:var(--space-sm);"></div>' for _ in range(lines)])
    html = f"""
    <div class="c-card">
        <div class="c-skeleton" style="height:24px; width:40%; margin-bottom:var(--space-md);"></div>
        {lines_html}
        <div class="c-skeleton" style="height:16px; width:60%; margin-top:var(--space-sm);"></div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
