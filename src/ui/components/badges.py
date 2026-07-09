import textwrap

def render_badge(label: str, variant: str = "neutral", icon: str = None) -> str:
    """Returns a styled HTML badge. Variants: primary, neutral, error, warning, success."""
    icon_html = f"<span class='material-symbols-outlined' style='font-size: 14px; margin-right: 4px;'>{icon}</span>" if icon else ""
    html = f"""
    <span class="c-badge c-badge--{variant}">
        {icon_html}{label}
    </span>
    """
    return textwrap.dedent(html).replace('\n', '')
