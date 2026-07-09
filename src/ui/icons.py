def render_icon(icon_name: str, size: int = 24) -> str:
    """Renders a Material Symbol Outlined icon."""
    return f"<span class='material-symbols-outlined' style='font-size:{size}px;'>{icon_name}</span>"
