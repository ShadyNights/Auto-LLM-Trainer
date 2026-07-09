def get_layout_css() -> str:
    return """
    /* =========================================================================
       3. LAYOUT & RESPONSIVE GRID
       ========================================================================= */
       
    /* Streamlit High-Level Stable Overrides */
    [data-testid="stSidebar"] {
        background-color: var(--c-layer-lowest) !important;
        border-right: 1px solid var(--c-outline-variant) !important;
    }

    /* Standard Grid Wrapper */
    .l-grid {
        display: grid;
        grid-template-columns: repeat(12, 1fr);
        gap: var(--space-md);
        max-width: 1440px;
        margin: 0 auto;
    }
    
    .l-section {
        margin-bottom: var(--space-xl);
        padding: 0;
    }
    """
