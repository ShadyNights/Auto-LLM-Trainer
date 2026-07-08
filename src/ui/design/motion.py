"""
Motion System.
Strictly limited to 6 semantic animation principles. No custom animations allowed.
"""

# Base easing curves
EASING_SMOOTH = "cubic-bezier(0.4, 0, 0.2, 1)"
EASING_BOUNCE = "cubic-bezier(0.175, 0.885, 0.32, 1.275)"

principles = {
    "entrance": f"250ms {EASING_SMOOTH}",
    "exit": f"200ms {EASING_SMOOTH}",
    "hover": f"150ms {EASING_SMOOTH}",
    "focus": f"100ms {EASING_SMOOTH}",
    "success": f"300ms {EASING_BOUNCE}",
    
    # CSS Animation definition for loading
    "loading": "pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite",
}

# The CSS Keyframes definition required for the loading principle
keyframes = """
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
"""
