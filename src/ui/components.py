import streamlit as st
import textwrap

def render_page_header(title: str, subtitle: str, icon: str = None, status_badge: str = None):
    """Universal page header."""
    icon_html = f"<span class='material-symbols-outlined' style='font-size: 32px; color: var(--color-accent-primary);'>{icon.replace(':material/', '').replace(':', '')}</span>" if icon else ""
    status_html = f"<span class='badge badge-success' style='margin-bottom: var(--space-2); display: inline-block;'>{status_badge}</span>" if status_badge else ""
    
    html = f"""
    <div style="padding: var(--space-6) 0; margin-bottom: var(--space-4);">
        {status_html}
        <div style="display: flex; align-items: center; gap: var(--space-2);">
            {icon_html}
            <h1 class="type-display" style="margin: 0;">{title}</h1>
        </div>
        <p class="type-body" style="max-width: 600px; margin-top: var(--space-2);">{subtitle}</p>
    </div>
    """
    st.html(textwrap.dedent(html))

def render_user_profile(name: str = "Modern AI Professional", role: str = "Pro Account", image_url: str = "https://lh3.googleusercontent.com/aida-public/AB6AXuDZvYxtOPSuoT8fq8jXUBiiXhZ-X9rqmlf4QguRuexgAIiXj3LzBAR5_5jejlXJFZ1MBujzaLbhBn9-cwjpNHAUS2-Z0qrUYV1iewStCRo58GW53xY2tVTeJcc4CepJxF2MPukPLmdB_SPFJhAYyiKMbCH2W4fQU2hzi8Co6VmuPizGxQ-B0hsJKQNvz-i7xzQrsoeiAklxqbIGbA7tfej0XD7vSfN6ko_ZYLbno-15lnRUk1-VkSOGIg"):
    """Sidebar user profile widget."""
    html = f"""
    <div style="display: flex; align-items: center; gap: var(--space-4); margin-bottom: var(--space-6);">
        <img src="{image_url}" alt="Profile" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover; border: 1px solid var(--color-border-default);" />
        <div>
            <div class="type-body" style="font-weight: 600; color: var(--color-text-primary); margin: 0; line-height: 1.2;">{name}</div>
            <div class="type-caption" style="color: var(--color-text-secondary); margin: 0; text-transform: none;">{role}</div>
        </div>
    </div>
    """
    st.html(textwrap.dedent(html))

def render_sidebar_link(label: str, icon: str, is_active: bool = False):
    """Sidebar navigation link styled identically to Tailwind mockups."""
    clean_icon = icon.replace(":material/", "").replace(":", "")
    
    if is_active:
        html = f"""
        <div style="display: flex; align-items: center; gap: var(--space-4); background-color: var(--color-accent-primary); color: #00363f; border-radius: var(--radius-lg); padding: var(--space-3) var(--space-4); margin-bottom: var(--space-2); cursor: pointer; box-shadow: 0 0 10px rgba(0,224,255,0.15); transition: all 0.2s;">
            <span class="material-symbols-outlined" style="font-size: 20px; font-variation-settings: 'FILL' 1;">{clean_icon}</span>
            <span class="type-body" style="margin: 0; color: #00363f; font-weight: 700; font-size: 14px;">{label}</span>
        </div>
        """
    else:
        html = f"""
        <div style="display: flex; align-items: center; gap: var(--space-4); color: var(--color-text-secondary); border-radius: var(--radius-lg); padding: var(--space-3) var(--space-4); margin-bottom: var(--space-2); cursor: pointer; transition: all 0.2s;" onmouseover="this.style.backgroundColor='var(--color-bg-surface-high)'; this.style.color='var(--color-text-primary)'" onmouseout="this.style.backgroundColor='transparent'; this.style.color='var(--color-text-secondary)'">
            <span class="material-symbols-outlined" style="font-size: 20px;">{clean_icon}</span>
            <span class="type-body" style="margin: 0; font-size: 14px;">{label}</span>
        </div>
        """
    st.html(textwrap.dedent(html))

def render_metric(label: str, value: str, icon: str, trend: str = None, trend_positive: bool = True):
    """Analytics metric card mimicking Tailwind grid layout."""
    trend_color = "var(--color-status-success)" if trend_positive else "var(--color-status-error)"
    trend_icon = "trending_up" if trend_positive else "trending_down"
    
    clean_icon = icon.replace(":material/", "").replace(":", "")
    
    trend_html = f"""
    <div style="display: flex; align-items: center; gap: var(--space-1); color: {trend_color}; margin-top: auto; padding-top: var(--space-2); border-top: 1px solid var(--color-border-hover);">
        <span class="material-symbols-outlined" style="font-size: 14px;">{trend_icon}</span>
        <span class="type-caption" style="text-transform: none;">{trend}</span>
    </div>
    """ if trend else ""

    html = f"""
    <div class="surface" style="padding: var(--space-4); display: flex; flex-direction: column; gap: var(--space-2); height: 100%;">
        <div style="display: flex; align-items: center; justify-content: space-between; color: var(--color-text-secondary);">
            <span class="type-caption">{label}</span>
            <span class="material-symbols-outlined" style="font-size: 18px;">{clean_icon}</span>
        </div>
        <div class="type-display" style="font-size: 32px; color: var(--color-text-primary); line-height: 1; margin-top: var(--space-1);">{value}</div>
        {trend_html}
    </div>
    """
    st.html(textwrap.dedent(html))

def render_badge(label: str, variant: str = "info"):
    """Semantic status badge."""
    st.html(f"<span class='badge badge-{variant}'>{label}</span>")

def render_ai_card(title: str, content: str, variant: str = "suggestion"):
    """
    Renders an AI interaction card.
    Variants: suggestion, thinking, warning, reasoning, citation, completion
    """
    icon_map = {
        "suggestion": "auto_awesome",
        "thinking": "psychology",
        "warning": "warning",
        "reasoning": "account_tree",
        "citation": "format_quote",
        "completion": "check_circle"
    }
    
    color_map = {
        "suggestion": "var(--color-accent-primary)",
        "thinking": "var(--color-text-muted)",
        "warning": "var(--color-status-warning)",
        "reasoning": "var(--color-status-info)",
        "citation": "var(--color-text-secondary)",
        "completion": "var(--color-status-success)"
    }
    
    icon = icon_map.get(variant, "info")
    color = color_map.get(variant, "var(--color-accent-primary)")
    
    cursor_class = "blinking-cursor" if variant == "thinking" else ""
    badge_html = f"<span class='badge badge-info' style='margin-left: var(--space-2); transform: scale(0.85); display: inline-block;'>AI Suggested</span>" if variant == "suggestion" else ""
    
    html = f"""
    <div class="surface" style="padding: var(--space-4); margin-bottom: var(--space-4); border-color: {color}40; background-color: var(--color-bg-surface-low);">
        <div style="display: flex; gap: var(--space-4);">
            <div style="color: {color}; margin-top: 2px;">
                <span class="material-symbols-outlined">{icon}</span>
            </div>
            <div>
                <div class="type-title" style="display: flex; align-items: center; margin-bottom: var(--space-2);">{title}{badge_html}</div>
                <div class="type-body {cursor_class}" style="color: var(--color-text-secondary); margin: 0;">{content}</div>
            </div>
        </div>
    </div>
    """
    st.html(textwrap.dedent(html))

def render_empty_state(title: str, description: str, icon: str = "folder_open"):
    """Renders a dead-end UI state."""
    clean_icon = icon.replace(":material/", "").replace(":", "")
    html = f"""
    <div style="text-align: center; padding: var(--space-10); border: 1px dashed var(--color-border-default); border-radius: var(--radius-lg);">
        <span class="material-symbols-outlined" style="font-size: 48px; color: var(--color-text-muted); margin-bottom: var(--space-4);">{clean_icon}</span>
        <h3 class="type-title" style="margin-bottom: var(--space-2);">{title}</h3>
        <p class="type-body">{description}</p>
    </div>
    """
    st.html(textwrap.dedent(html))

def render_card(title: str, content: str, interactive: bool = False):
    """Renders a structural Surface primitive."""
    surface_class = "surface surface-interactive" if interactive else "surface"
    html = f"""
    <div class="{surface_class}" style="padding: var(--space-4); margin-bottom: var(--space-4);">
        <h4 class="type-title" style="margin-bottom: var(--space-2);">{title}</h4>
        <p class="type-body" style="margin-bottom: 0; white-space: pre-wrap;">{content}</p>
    </div>
    """
    st.html(textwrap.dedent(html))
