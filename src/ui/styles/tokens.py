def get_tokens_css() -> str:
    return """
    /* =========================================================================
       1. TOKENS (Foundation, Semantic, Component, Utility)
       ========================================================================= */
    :root {
        /* Foundation Tokens: Colors */
        --c-brand-100: #BAF2FF;
        --c-brand-500: #00E0FF;
        --c-brand-700: #A5EEFF;
        --c-brand-900: #00DAF8;
        
        --c-surface-0: #0B1326;
        --c-surface-1: #060E20;
        --c-surface-2: #131B2E;
        --c-surface-3: #171F33;
        --c-surface-4: #222A3D;
        --c-surface-5: #2D3449;
        
        --c-support-100: #BCC7DE;
        --c-support-500: #3E495D;
        --c-support-900: #D8E3FB;
        
        --c-accent-100: #FFE6B6;
        --c-accent-500: #FEC42E;
        
        --c-status-error: #FFB4AB;
        --c-status-error-dark: #93000A;
        --c-status-success: #81C995;
        --c-status-warning: #FDD663;
        
        --c-outline-high: #859397;
        --c-outline-low: #3B494C;

        /* Foundation Tokens: Spacing (4px Baseline) */
        --space-0: 0px;
        --space-1: 4px;
        --space-2: 8px;
        --space-3: 12px;
        --space-4: 16px;
        --space-5: 20px;
        --space-6: 24px;
        --space-8: 32px;
        --space-10: 40px;
        --space-16: 64px;

        /* Foundation Tokens: Radius */
        --radius-sm: 2px;
        --radius-md: 4px;
        --radius-lg: 8px;
        --radius-xl: 12px;
        --radius-pill: 9999px;

        /* Foundation Tokens: Opacity */
        --opacity-hover: 0.08;
        --opacity-focus: 0.12;
        --opacity-disabled: 0.38;
        --opacity-scrim: 0.60;
        
        /* Foundation Tokens: Typography Sizes */
        --text-display: 48px;
        --text-headline: 24px;
        --text-title: 20px;
        --text-body: 16px;
        --text-label: 12px;
        --text-code: 13px;

        /* ========================================= */
        /* Semantic Tokens (Dark Theme - Default)    */
        /* ========================================= */
        --t-color-primary: var(--c-brand-100);
        --t-color-primary-container: var(--c-brand-500);
        --t-color-surface-tint: var(--c-brand-900);
        
        --t-bg-base: var(--c-surface-0);
        --t-layer-lowest: var(--c-surface-1);
        --t-layer-low: var(--c-surface-2);
        --t-layer-base: var(--c-surface-3);
        --t-layer-high: var(--c-surface-4);
        --t-layer-highest: var(--c-surface-5);
        
        --t-color-secondary: var(--c-support-100);
        --t-color-tertiary: var(--c-accent-100);
        
        --t-color-error: var(--c-status-error);
        --t-color-success: var(--c-status-success);
        --t-color-warning: var(--c-status-warning);
        
        --t-color-outline: var(--c-outline-high);
        --t-color-outline-variant: var(--c-outline-low);
        
        /* Focus Ring */
        --t-focus-ring: 0 0 0 2px var(--t-bg-base), 0 0 0 4px var(--t-color-primary-container);

        /* Elevation (Levels 0-4) */
        --t-shadow-level-1: 0 1px 2px rgba(0,0,0,0.3);
        --t-shadow-level-2: 0 4px 6px rgba(0,0,0,0.4);
        --t-shadow-level-3: 0 10px 15px rgba(0,0,0,0.5);
        --t-shadow-level-4: 0 20px 25px rgba(0,0,0,0.6);
        --t-shadow-glow: 0 0 15px rgba(0,224,255,0.2);
    }

    /* Light Theme Overrides */
    @media (prefers-color-scheme: light) {
        :root {
            /* Invert semantic surfaces for light mode */
            --t-bg-base: #FFFFFF;
            --t-layer-lowest: #F8F9FA;
            --t-layer-low: #F1F3F5;
            --t-layer-base: #E9ECEF;
            --t-layer-high: #DEE2E6;
            --t-layer-highest: #CED4DA;
            
            --t-color-primary: #005F73;
            --t-color-secondary: #495057;
            --t-color-outline: #ADB5BD;
            --t-color-outline-variant: #DEE2E6;
            
            --t-shadow-level-1: 0 1px 2px rgba(0,0,0,0.05);
            --t-shadow-level-2: 0 4px 6px rgba(0,0,0,0.1);
        }
    }
    """
