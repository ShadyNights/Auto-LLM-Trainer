def get_animations_css() -> str:
    return """
    /* =========================================================================
       5. ANIMATIONS & MOTION
       ========================================================================= */

    /* Pulse */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Blink */
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    .anim-blink {
        animation: blink 1s infinite;
        display: inline-block;
        width: 8px;
        background-color: var(--c-primary-container);
        vertical-align: middle;
        height: 1em;
        margin-left: 4px;
    }
    """
