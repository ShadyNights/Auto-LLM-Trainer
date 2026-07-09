def get_utilities_css() -> str:
    return """
    /* =========================================================================
       6. UTILITIES
       ========================================================================= */
       
    .text-center { text-align: center; }
    .text-right { text-align: right; }
    
    .text-primary { color: var(--t-color-primary) !important; }
    .text-secondary { color: var(--t-color-secondary) !important; }
    .text-tertiary { color: var(--t-color-tertiary) !important; }
    
    .w-full { width: 100%; }
    .h-full { height: 100%; }
    
    .flex-1 { flex: 1; }
    
    .mt-0 { margin-top: 0 !important; }
    .mb-0 { margin-bottom: 0 !important; }
    
    /* Visually hidden for screen readers */
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border-width: 0;
    }
    """
