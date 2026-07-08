import streamlit as st

def render_hero(title: str, subtitle: str, icon: str = "✈️"):
    """Renders a simple, professional page header."""
    st.markdown(f"""
    <div style="padding: var(--space-6) 0; margin-bottom: var(--space-4);">
        <h1 class="type-display">{icon} {title}</h1>
        <p class="type-body" style="max-width: 600px;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_page_section(title: str, subtitle: str = None, icon: str = None):
    """Renders a consistent section header."""
    icon_html = f"<span style='margin-right: var(--space-2);'>{icon}</span>" if icon else ""
    subtitle_html = f"<p class='type-caption' style='margin-top: var(--space-1);'>{subtitle}</p>" if subtitle else ""
    
    st.markdown(f"""
    <div style="margin-bottom: var(--space-4);">
        <h3 class="type-title" style="margin-bottom: 0;">{icon_html}{title}</h3>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)

def render_metric(label: str, value: str, delta: str = None, is_positive: bool = True):
    """Renders an atomic number representation."""
    delta_color = "var(--color-status-success)" if is_positive else "var(--color-status-error)"
    delta_html = f"<div class='type-caption' style='color: {delta_color};'>{delta}</div>" if delta else ""
    
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; gap: var(--space-2);">
        <div class="type-caption">{label}</div>
        <div class="type-heading">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def render_card(title: str, content: str, interactive: bool = False):
    """Renders a structural Surface primitive."""
    surface_class = "surface surface-interactive" if interactive else "surface"
    st.markdown(f"""
    <div class="{surface_class}" style="padding: var(--space-4); margin-bottom: var(--space-4);">
        <h4 class="type-title" style="margin-bottom: var(--space-2);">{title}</h4>
        <p class="type-body" style="margin-bottom: 0;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

def render_badge(label: str, variant: str = "info"):
    """
    Renders a semantic status badge.
    Variants: success, warning, error, info
    """
    st.markdown(f"""
    <span class="badge badge-{variant}">{label}</span>
    """, unsafe_allow_html=True)

def render_empty_state(title: str, description: str, icon: str = "📂"):
    """Renders a dead-end UI state. Must be followed by a Streamlit button CTA in the app script."""
    st.markdown(f"""
    <div style="text-align: center; padding: var(--space-10); border: 1px dashed var(--color-border-default); border-radius: var(--radius-lg);">
        <div class="type-display" style="margin-bottom: var(--space-4); color: var(--color-text-muted);">{icon}</div>
        <h3 class="type-title" style="margin-bottom: var(--space-2);">{title}</h3>
        <p class="type-body">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_ai_message(message: str, is_user: bool = False):
    """Renders an AI interaction system node (Prompt or Response)."""
    bg_color = "var(--color-bg-surface-raised)" if is_user else "transparent"
    align = "right" if is_user else "left"
    margin = "margin-left: auto;" if is_user else "margin-right: auto;"
    
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; text-align: {align}; margin-bottom: var(--space-4);">
        <div style="background-color: {bg_color}; padding: var(--space-3) var(--space-4); border-radius: var(--radius-lg); max-width: 80%; {margin}">
            <p class="type-body" style="margin-bottom: 0;">{message}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
