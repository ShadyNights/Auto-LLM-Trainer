import streamlit as st
from typing import Optional

def get_components_css() -> str:
    """Returns the CSS string for the reusable components."""
    return """
    /* =========================================================================
       REUSABLE UI COMPONENTS
       ========================================================================= */
    .c-card {
        background-color: var(--c-layer-base);
        border: 1px solid var(--c-outline-variant);
        border-radius: var(--radius-xl);
        padding: var(--space-md);
        box-shadow: var(--shadow-sm);
        transition: box-shadow 300ms ease, transform 300ms ease;
    }
    .c-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
    .c-card--active-glow { box-shadow: var(--shadow-glow); border-color: var(--c-primary-container); }

    .c-badge {
        display: inline-flex; align-items: center; gap: var(--space-xs);
        padding: 2px 8px; border-radius: var(--radius-full);
        font-family: 'Geist', sans-serif; font-size: var(--text-label); font-weight: 500;
        letter-spacing: 0.05em; line-height: 1.2; border: 1px solid transparent; white-space: nowrap;
    }
    .c-badge--error { background-color: var(--c-error-container); color: var(--c-error); border-color: rgba(255, 180, 171, 0.3); }
    .c-badge--primary { background-color: rgba(0, 224, 255, 0.15); color: var(--c-primary-container); border-color: rgba(0, 224, 255, 0.3); }
    .c-badge--neutral { background-color: var(--c-layer-highest); color: var(--c-secondary); }

    .c-skeleton { background-color: var(--c-layer-high); border-radius: var(--radius-default); animation: pulse 2s infinite; }
    .c-skeleton--line { height: 16px; width: 100%; margin-bottom: var(--space-sm); }
    .c-skeleton--title { height: 24px; width: 40%; margin-bottom: var(--space-md); }
    .c-skeleton--short { height: 16px; width: 60%; margin-top: var(--space-sm); }
    
    .c-metric-card {
        background-color: var(--c-layer-base);
        border: 1px solid var(--c-outline-variant);
        border-radius: var(--radius-xl);
        padding: var(--space-md);
        display: flex; flex-direction: column; gap: var(--space-xs);
        box-shadow: var(--shadow-sm);
        transition: box-shadow 300ms ease, transform 300ms ease;
    }
    .c-metric-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
    .c-metric-card__header { display: flex; align-items: center; justify-content: space-between; }
    .c-metric-card__title { font-family: 'Geist', sans-serif; font-size: var(--text-label); color: var(--c-secondary); text-transform: uppercase; letter-spacing: 0.05em; display:flex; align-items:center; gap:4px; }
    .c-metric-card__value { font-size: var(--text-headline); font-weight: 600; color: var(--c-primary); line-height: 1.1; margin-top: var(--space-xs); }
    .c-metric-card__context { font-size: var(--text-label); color: var(--c-outline); margin-top: var(--space-xs); }

    .c-empty-state {
        text-align: center;
        padding: var(--space-xl) var(--space-md);
        background-color: transparent;
        border: 1px dashed var(--c-outline-variant);
        border-radius: var(--radius-xl);
    }
    .c-empty-state__icon { font-size: 32px; color: var(--c-secondary); margin-bottom: var(--space-md); }

    .c-meta-label { margin: 0; color: var(--c-secondary); }
    .c-meta-value { font-family: monospace; margin: 0; color: var(--c-primary); }

    /* Streamlit Global Overrides (Tables & Inputs) */
    [data-testid="stTable"], [data-testid="stDataFrame"] { font-family: 'Geist', sans-serif; }
    [data-testid="stTable"] th, [data-testid="stDataFrame"] th { background-color: var(--c-layer-high) !important; color: var(--c-primary) !important; font-weight: 600 !important; }
    [data-testid="stTable"] tr:nth-child(even) { background-color: var(--c-layer-low) !important; }
    """

def render_card(content_html: str, active_glow: bool = False, class_name: str = ""):
    classes = ["c-card"]
    if active_glow: classes.append("c-card--active-glow")
    if class_name: classes.append(class_name)
    st.markdown(f'<div class="{" ".join(classes)}">{content_html}</div>', unsafe_allow_html=True)

def render_badge(text: str, variant: str = "neutral", class_name: str = "") -> str:
    return f'<span class="c-badge c-badge--{variant} {class_name}">{text}</span>'

def render_metric(title: str, value: str, icon: str = "", trend_label: Optional[str] = None, variant: str = "neutral", context: str = ""):
    trend_html = render_badge(trend_label, variant=variant) if trend_label else ""
    icon_html = f"<span class='material-symbols-outlined' style='font-size:16px;'>{icon}</span>" if icon else ""
    context_html = f"<div class='c-metric-card__context'>{context}</div>" if context else ""
    
    st.markdown(f"""
    <div class="c-metric-card">
        <div class="c-metric-card__header">
            <div class="c-metric-card__title">{icon_html} {title}</div>
            {trend_html}
        </div>
        <div class="c-metric-card__value">{value}</div>
        {context_html}
    </div>
    """, unsafe_allow_html=True)

def render_empty_state(title: str, description: str, icon: str = "block"):
    st.markdown(f"""
    <div class="c-empty-state">
        <span class="material-symbols-outlined c-empty-state__icon">{icon}</span>
        <h3>{title}</h3>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_loading(lines: int = 3):
    lines_html = "".join(['<div class="c-skeleton c-skeleton--line"></div>' for _ in range(lines)])
    st.markdown(f"""
    <div class="c-card">
        <div class="c-skeleton c-skeleton--title"></div>
        {lines_html}
        <div class="c-skeleton c-skeleton--short"></div>
    </div>
    """, unsafe_allow_html=True)

def render_provider_indicator(provider_name: str, status: str = "primary"):
    """Renders a provider indicator badge."""
    return render_badge(f"Provider: {provider_name}", variant=status)

def render_version_indicator(version: str):
    """Renders a version indicator badge."""
    return render_badge(f"v{version}", variant="neutral")

def render_progress_indicator(value: int, text: str):
    """Renders a progress state using native Streamlit."""
    st.progress(value, text=text)
