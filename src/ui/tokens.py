def get_tokens_css() -> str:
    """Returns the CSS string for the strict baseline tokens."""
    return """
    /* =========================================================================
       1. DESIGN TOKENS (Strict Baseline)
       ========================================================================= */
    :root {
        /* Colors: Primary */
        --c-primary: #BAF2FF;
        --c-primary-container: #00E0FF;
        --c-primary-fixed: #A5EEFF;
        --c-primary-fixed-dim: #00DAF8;
        --c-surface-tint: #00DAF8;
        
        /* Colors: Background */
        --c-background: #0B1326;
        --c-surface: #0B1326;
        --c-surface-bright: #31394D;
        --c-surface-dim: #0B1326;
        
        /* Colors: Surface Layers */
        --c-layer-lowest: #060E20;
        --c-layer-low: #131B2E;
        --c-layer-base: #171F33;
        --c-layer-high: #222A3D;
        --c-layer-highest: #2D3449;
        
        /* Colors: Secondary & Tertiary */
        --c-secondary: #BCC7DE;
        --c-tertiary: #FFE6B6;
        
        /* Colors: Semantic Error & Outline */
        --c-error: #FFB4AB;
        --c-error-container: #93000A;
        --c-outline: #859397;
        --c-outline-variant: #3B494C;

        /* Spacing System */
        --space-base: 4px;
        --space-xs: 4px;
        --space-sm: 8px;
        --space-md: 16px;
        --space-lg: 24px;
        --space-xl: 40px;

        /* Border Radius */
        --radius-default: 2px;
        --radius-lg: 4px;
        --radius-xl: 8px;
        --radius-full: 12px;
        
        /* Typography System */
        --text-display: 48px;
        --text-headline: 24px;
        --text-body: 16px;
        --text-label: 12px;
        --text-code: 13px;

        /* Elevation */
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
        --shadow-md: 0 4px 6px rgba(0,0,0,0.4);
        --shadow-glow: 0 0 15px rgba(0,224,255,0.2);
    }
    """
