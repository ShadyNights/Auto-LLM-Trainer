"""
Typography System.
Strictly limited to 5 levels to prevent duplication and inconsistency.
"""

# Base font stack prioritizes clarity and modern SaaS sans-serifs.
FONT_FAMILY = "'Inter', 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"

levels = {
    "display": {
        "font-size": "2.5rem",
        "font-weight": "700",
        "line-height": "1.2",
        "letter-spacing": "-0.02em",
    },
    "heading": {
        "font-size": "1.5rem",
        "font-weight": "600",
        "line-height": "1.3",
        "letter-spacing": "-0.01em",
    },
    "title": {
        "font-size": "1.125rem",
        "font-weight": "600",
        "line-height": "1.4",
        "letter-spacing": "0",
    },
    "body": {
        "font-size": "1rem",
        "font-weight": "400",
        "line-height": "1.6",
        "letter-spacing": "0",
    },
    "caption": {
        "font-size": "0.875rem",
        "font-weight": "500",
        "line-height": "1.5",
        "letter-spacing": "0.01em",
        "text-transform": "uppercase",
    }
}
