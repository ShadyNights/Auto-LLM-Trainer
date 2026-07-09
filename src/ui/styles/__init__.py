from .tokens import get_tokens_css
from .base import get_base_css
from .layout import get_layout_css
from .components import get_components_css
from .animations import get_animations_css
from .utilities import get_utilities_css

def get_global_css() -> str:
    """Aggregates all CSS modules into a single stylesheet."""
    css = "\\n".join([
        get_tokens_css(),
        get_base_css(),
        get_layout_css(),
        get_components_css(),
        get_animations_css(),
        get_utilities_css()
    ])
    return f"<style>\\n{css}\\n</style>"
