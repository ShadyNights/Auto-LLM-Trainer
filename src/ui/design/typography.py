"""
Typography System.
Strictly limited to 5 levels to prevent duplication and inconsistency.
Fonts extracted from Design Specification.
"""

FONT_FAMILY = "'Geist', sans-serif"
FONT_DISPLAY = "'Space Grotesk', sans-serif"
FONT_CODE = "'JetBrains Mono', monospace"

levels = {
    "display": {
        "font-family": FONT_DISPLAY,
        "font-size": "48px",
        "font-weight": "700",
        "line-height": "1.1",
        "letter-spacing": "-0.02em",
    },
    "heading": {
        "font-family": FONT_FAMILY,
        "font-size": "24px",
        "font-weight": "600",
        "line-height": "1.4",
        "letter-spacing": "0",
    },
    "title": {
        "font-family": FONT_FAMILY,
        "font-size": "18px",
        "font-weight": "600",
        "line-height": "1.4",
        "letter-spacing": "0",
    },
    "body": {
        "font-family": FONT_FAMILY,
        "font-size": "16px",
        "font-weight": "400",
        "line-height": "1.6",
        "letter-spacing": "0",
    },
    "caption": {
        "font-family": FONT_FAMILY,
        "font-size": "12px",
        "font-weight": "500",
        "line-height": "1.0",
        "letter-spacing": "0.05em",
        "text-transform": "uppercase",
    }
}
