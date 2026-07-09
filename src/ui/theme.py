def get_theme_css() -> str:
    """Returns the CSS string for the baseline theme and typography configuration."""
    return """
    /* =========================================================================
       2. THEME & BASE CONFIGURATION
       ========================================================================= */
    .stApp {
        background-color: var(--c-background) !important;
        color: var(--c-secondary) !important;
        font-family: 'Geist', -apple-system, sans-serif;
        font-size: var(--text-body);
        line-height: 1.6;
        font-weight: 400;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--c-primary);
        margin: 0 0 var(--space-sm) 0;
    }
    
    h1 { font-family: 'Space Grotesk', sans-serif; font-size: var(--text-display); font-weight: 700; line-height: 1.1; }
    h2, h3 { font-size: var(--text-headline); font-weight: 600; line-height: 1.2; }

    p {
        color: var(--c-secondary);
        margin: 0 0 var(--space-md) 0;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace;
        font-size: var(--text-code);
        font-weight: 400;
    }

    *:focus-visible {
        outline: 1px solid var(--c-outline) !important;
        box-shadow: 0 0 0 3px var(--c-surface-tint) !important;
    }
    """
