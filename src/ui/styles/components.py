def get_components_css() -> str:
    return """
    /* =========================================================================
       4. COMPONENT LIBRARY PRIMITIVES
       ========================================================================= */

    /* Cards & Surfaces */
    .c-surface {
        background-color: var(--t-layer-base);
        border: 1px solid var(--t-color-outline-variant);
        border-radius: var(--radius-lg);
        padding: var(--comp-padding-y, var(--space-4)) var(--comp-padding-x, var(--space-4));
        box-shadow: var(--t-shadow-level-1);
        transition: transform var(--duration-fast) var(--ease-standard), 
                    box-shadow var(--duration-fast) var(--ease-standard);
    }
    .c-surface--hoverable:hover {
        transform: translateY(-2px);
        box-shadow: var(--t-shadow-level-2);
        border-color: var(--t-color-outline);
    }
    
    .c-surface--ai-glow {
        box-shadow: var(--t-shadow-glow);
        border-color: var(--t-color-primary-container);
    }

    /* Dividers */
    .c-divider {
        height: 1px;
        background-color: var(--t-color-outline-variant);
        margin: var(--space-4) 0;
        width: 100%;
        border: none;
    }

    /* Badges */
    .c-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--space-1);
        padding: 2px 8px;
        border-radius: var(--radius-pill);
        font-size: var(--text-label);
        font-weight: 500;
        line-height: 1.2;
        border: 1px solid transparent;
        white-space: nowrap;
    }
    .c-badge--success { background-color: rgba(129, 201, 149, 0.15); color: var(--t-color-success); border-color: rgba(129, 201, 149, 0.3); }
    .c-badge--error { background-color: rgba(255, 180, 171, 0.15); color: var(--t-color-error); border-color: rgba(255, 180, 171, 0.3); }
    .c-badge--warning { background-color: rgba(253, 214, 99, 0.15); color: var(--t-color-warning); border-color: rgba(253, 214, 99, 0.3); }
    .c-badge--neutral { background-color: var(--t-layer-highest); color: var(--t-color-secondary); }
    .c-badge--ai { background-color: rgba(0, 224, 255, 0.15); color: var(--t-color-primary-container); border-color: rgba(0, 224, 255, 0.3); }

    /* Empty States */
    .c-empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: var(--space-10) var(--space-4);
        background-color: transparent;
        border: 1px dashed var(--t-color-outline-variant);
        border-radius: var(--radius-lg);
    }
    .c-empty-state__icon {
        font-size: 32px;
        color: var(--t-color-secondary);
        margin-bottom: var(--space-4);
    }
    
    /* Skeleton Loaders (Processing States) */
    .c-skeleton {
        background-color: var(--t-layer-high);
        border-radius: var(--radius-md);
        animation: pulse var(--anim-pulse-dur, 2s) infinite cubic-bezier(0.4, 0, 0.6, 1);
    }
    
    /* Metrics */
    .c-metric {
        display: flex;
        flex-direction: column;
        gap: var(--space-1);
    }
    .c-metric__title {
        font-size: var(--text-label);
        color: var(--t-color-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .c-metric__value {
        font-size: var(--text-headline);
        font-weight: 600;
        color: var(--t-color-primary);
        line-height: 1.1;
    }
    
    /* AI Transparency Footer */
    .c-ai-footer {
        display: flex;
        flex-wrap: wrap;
        gap: var(--space-4);
        font-size: var(--text-label);
        color: var(--t-color-secondary);
        background-color: var(--t-layer-lowest);
        padding: var(--space-2) var(--space-4);
        border-radius: 0 0 var(--radius-lg) var(--radius-lg);
        border-top: 1px solid var(--t-color-outline-variant);
        align-items: center;
    }
    .c-ai-footer__item {
        display: flex;
        align-items: center;
        gap: var(--space-1);
    }
    """
