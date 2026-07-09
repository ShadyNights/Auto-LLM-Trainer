def get_animations_css() -> str:
    return """
    /* =========================================================================
       5. ANIMATIONS & MOTION
       ========================================================================= */

    /* Pulse animation for skeletons */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Blinking text cursor for AI generation */
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    .anim-blink {
        animation: blink 1s infinite;
        display: inline-block;
        width: 8px;
        background-color: var(--t-color-primary-container);
        vertical-align: middle;
        height: 1em;
        margin-left: 4px;
    }
    
    /* Accessible Reduced Motion Rules */
    @media (prefers-reduced-motion: reduce) {
        *, ::before, ::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
        .anim-blink {
            opacity: 1 !important;
        }
        .c-skeleton {
            opacity: 0.7 !important;
        }
    }
    """
