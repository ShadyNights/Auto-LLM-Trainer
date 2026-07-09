def get_animations_css() -> str:
    """Returns the CSS string for motion utilities."""
    return """
    /* =========================================================================
       MOTION UTILITIES
       ========================================================================= */
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
    """
