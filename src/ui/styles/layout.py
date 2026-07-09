def get_layout_css() -> str:
    return """
    /* =========================================================================
       3. LAYOUT & DENSITY MODES
       ========================================================================= */
       
    /* Streamlit High-Level Stable Overrides */
    [data-testid="stSidebar"] {
        background-color: var(--t-layer-lowest) !important;
        border-right: 1px solid var(--t-color-outline-variant) !important;
        min-width: 280px !important;
    }

    /* Density Modes (Applied to custom HTML components) */
    .density-compact {
        --comp-padding-x: var(--space-2);
        --comp-padding-y: var(--space-2);
        --comp-gap: var(--space-2);
    }
    
    .density-comfortable {
        --comp-padding-x: var(--space-4);
        --comp-padding-y: var(--space-4);
        --comp-gap: var(--space-4);
    }

    /* Custom Layout Primitives */
    .l-stack {
        display: flex;
        flex-direction: column;
        gap: var(--comp-gap, var(--space-4));
    }
    
    .l-stack-h {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: var(--comp-gap, var(--space-4));
    }
    
    .l-grid {
        display: grid;
        grid-template-columns: repeat(12, 1fr);
        gap: var(--space-4);
    }
    
    .l-section {
        margin-bottom: var(--space-10);
        padding: 0;
    }
    """
