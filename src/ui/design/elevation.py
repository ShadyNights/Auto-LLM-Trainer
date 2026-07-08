"""
Elevation System.
Only 4 levels allowed: Surface, Raised, Floating, Overlay.
"""

levels = {
    "surface": {
        "box-shadow": "none",
        "z-index": "0",
    },
    "raised": {
        "box-shadow": "0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2)",
        "z-index": "10",
    },
    "floating": {
        "box-shadow": "0 4px 6px -1px rgba(0,0,0,0.4), 0 2px 4px -1px rgba(0,0,0,0.3)",
        "z-index": "40",
    },
    "overlay": {
        "box-shadow": "0 20px 25px -5px rgba(0,0,0,0.5), 0 10px 10px -5px rgba(0,0,0,0.4)",
        "z-index": "50",
    }
}
