import streamlit as st

def render_hero(title: str, subtitle: str, icon: str = "✈️"):
    """Renders a simple, professional page header."""
    st.markdown(f"""
    <div class="hero">
        <h1>{icon} {title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_page_section(title: str, subtitle: str = None, icon: str = None):
    """Renders a consistent section header."""
    icon_html = f"<span style='margin-right: 8px;'>{icon}</span>" if icon else ""
    subtitle_html = f"<p class='text-muted' style='margin-top: 4px;'>{subtitle}</p>" if subtitle else ""
    
    st.markdown(f"""
    <div style="margin-bottom: var(--spacing-4);">
        <h3 style="margin-bottom: 0;">{icon_html}{title}</h3>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)

def render_card(content_html: str, raised: bool = False):
    """Renders content inside a surface card."""
    css_class = "card card--raised" if raised else "card"
    st.markdown(f"""
    <div class="{css_class}">
        {content_html}
    </div>
    """, unsafe_allow_html=True)

def render_metric(title: str, value: str, label: str = None, status: str = "neutral"):
    """
    Renders a professional metric card.
    status: 'success', 'warning', 'error', 'info', 'neutral'
    """
    label_html = ""
    if label:
        label_html = f"""
        <div class="metric-footer">
            <span class="badge badge--{status}">{label}</span>
        </div>
        """
        
    st.markdown(f"""
    <div class="card metric">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        {label_html}
    </div>
    """, unsafe_allow_html=True)

def render_badge(text: str, status: str = "neutral") -> str:
    """Returns HTML for a status badge inline."""
    return f'<span class="badge badge--{status}">{text}</span>'

def render_empty_state(icon: str, title: str, description: str):
    """Renders a dashed-border empty state for missing data."""
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-state-icon">{icon}</div>
        <h3>{title}</h3>
        <p class="text-secondary">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_skeleton_loader():
    """Renders a lightweight pulse animation for loading content."""
    st.markdown("""
    <div class="card">
        <div class="skeleton skeleton-title"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text-short"></div>
        <br/>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text-short"></div>
    </div>
    """, unsafe_allow_html=True)
