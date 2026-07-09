def get_base_css() -> str:
    return """
    /* =========================================================================
       2. BASE & TYPOGRAPHY
       ========================================================================= */
    .stApp {
        background-color: var(--t-bg-base) !important;
        color: var(--t-color-primary) !important;
        font-family: 'Geist', -apple-system, sans-serif;
        font-size: var(--text-body);
        line-height: 1.6;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--t-color-primary);
        margin: 0 0 var(--space-2) 0;
        font-weight: 600;
    }
    
    h1 { font-family: 'Space Grotesk', sans-serif; font-size: var(--text-display); font-weight: 700; line-height: 1.1; }
    h2 { font-size: var(--text-headline); line-height: 1.2; letter-spacing: -0.01em; }
    h3 { font-size: var(--text-title); line-height: 1.4; }

    p {
        color: var(--t-color-secondary);
        margin: 0 0 var(--space-4) 0;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace;
        font-size: var(--text-code);
    }

    /* Accessibility: Focus Rings on all interactive elements */
    *:focus-visible {
        outline: none !important;
        box-shadow: var(--t-focus-ring) !important;
        border-radius: var(--radius-sm);
    }
    
    /* Global scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
        background-color: transparent;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background-color: var(--t-color-outline-variant);
        border-radius: var(--radius-pill);
    }
    ::-webkit-scrollbar-thumb:hover {
        background-color: var(--t-color-outline);
    }
    """
