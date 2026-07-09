def get_components_css() -> str:
    return """
    /* =========================================================================
       4. COMPONENT LIBRARY PRIMITIVES (Strict Baseline)
       ========================================================================= */

    /* Cards */
    .c-card {
        background-color: var(--c-layer-base);
        border: 1px solid var(--c-outline-variant);
        border-radius: var(--radius-xl); /* 8px */
        padding: var(--space-md);
        box-shadow: var(--shadow-sm); /* Border + Shadow */
        transition: box-shadow 300ms ease, transform 300ms ease;
    }
    
    .c-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }
    
    .c-card--active-glow {
        box-shadow: var(--shadow-glow);
        border-color: var(--c-primary-container);
    }

    /* Badges */
    .c-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--space-xs);
        padding: 2px 8px;
        border-radius: var(--radius-full);
        font-family: 'Geist', sans-serif;
        font-size: var(--text-label);
        font-weight: 500;
        letter-spacing: 0.05em;
        line-height: 1.2;
        border: 1px solid transparent;
        white-space: nowrap;
    }
    .c-badge--error { background-color: var(--c-error-container); color: var(--c-error); border-color: rgba(255, 180, 171, 0.3); }
    .c-badge--primary { background-color: rgba(0, 224, 255, 0.15); color: var(--c-primary-container); border-color: rgba(0, 224, 255, 0.3); }
    .c-badge--neutral { background-color: var(--c-layer-highest); color: var(--c-secondary); }

    /* Empty States (Not explicitly defined in spec, mapped to basic container) */
    .c-empty-state {
        text-align: center;
        padding: var(--space-xl) var(--space-md);
        background-color: transparent;
        border: 1px dashed var(--c-outline-variant);
        border-radius: var(--radius-xl);
    }
    
    /* Skeleton Loaders */
    .c-skeleton {
        background-color: var(--c-layer-high);
        border-radius: var(--radius-default);
        animation: pulse 2s infinite;
    }
    
    /* Metrics */
    .c-metric {
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
    }
    .c-metric__title {
        font-family: 'Geist', sans-serif;
        font-size: var(--text-label);
        color: var(--c-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .c-metric__value {
        font-size: var(--text-headline);
        font-weight: 600;
        color: var(--c-primary);
        line-height: 1.1;
    }
    """
