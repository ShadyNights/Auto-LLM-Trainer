import streamlit as st
from src.ui.design import tokens, themes, typography, elevation, motion

def _generate_css_variables() -> str:
    """Compiles the Python design tokens into CSS custom properties."""
    css_vars = []
    
    # 1. Semantic Colors
    for key, value in themes.dark_theme.items():
        css_name = f"--{key.replace('.', '-')}"
        css_vars.append(f"        {css_name}: {value};")
        
    # 2. Spacing
    for key, value in tokens.spacing.items():
        css_vars.append(f"        --space-{key}: {value};")
        
    # 3. Radius
    for key, value in tokens.radius.items():
        css_vars.append(f"        --radius-{key}: {value};")
        
    # 4. Motion
    for key, value in motion.principles.items():
        if key != "loading": # Loading is a complex animation, not a single easing string
            css_vars.append(f"        --motion-{key}: {value};")

    return "\n".join(css_vars)


def get_global_css() -> str:
    """Generates the unified Design System CSS."""
    
    css = f"""
<style>
    /* =========================================================================
       1. COMPILED DESIGN TOKENS
       ========================================================================= */
    :root {{
{_generate_css_variables()}
    }}

    /* Accessibility: Reduced Motion */
    @media (prefers-reduced-motion: reduce) {{
        *, ::before, ::after {{
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }}
    }}
    
    {motion.keyframes}

    /* =========================================================================
       2. TYPOGRAPHY (5-Level System)
       ========================================================================= */
       
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    .stApp {{
        background-color: var(--color-bg-base);
        color: var(--color-text-primary);
        font-family: {typography.FONT_FAMILY};
        -webkit-font-smoothing: antialiased;
    }}
    
    /* Apply Typography Levels */
    .type-display {{
        font-family: {typography.levels['display']['font-family']};
        font-size: {typography.levels['display']['font-size']};
        font-weight: {typography.levels['display']['font-weight']};
        line-height: {typography.levels['display']['line-height']};
        letter-spacing: {typography.levels['display']['letter-spacing']};
    }}
    h1, .type-heading {{
        font-family: {typography.levels['heading']['font-family']};
        font-size: {typography.levels['heading']['font-size']};
        font-weight: {typography.levels['heading']['font-weight']};
        line-height: {typography.levels['heading']['line-height']};
        letter-spacing: {typography.levels['heading']['letter-spacing']};
        color: var(--color-text-primary);
    }}
    h2, h3, .type-title {{
        font-family: {typography.levels['title']['font-family']};
        font-size: {typography.levels['title']['font-size']};
        font-weight: {typography.levels['title']['font-weight']};
        line-height: {typography.levels['title']['line-height']};
        color: var(--color-text-primary);
    }}
    p, .type-body {{
        font-family: {typography.levels['body']['font-family']};
        font-size: {typography.levels['body']['font-size']};
        font-weight: {typography.levels['body']['font-weight']};
        line-height: {typography.levels['body']['line-height']};
        color: var(--color-text-secondary);
    }}
    small, .type-caption {{
        font-family: {typography.levels['caption']['font-family']};
        font-size: {typography.levels['caption']['font-size']};
        font-weight: {typography.levels['caption']['font-weight']};
        text-transform: {typography.levels['caption']['text-transform']};
        letter-spacing: {typography.levels['caption']['letter-spacing']};
        color: var(--color-text-muted);
    }}

    /* =========================================================================
       3. COMPONENT PRIMITIVES & ELEVATION
       ========================================================================= */
       
    .surface {{
        background-color: var(--color-bg-surface);
        border: 1px solid var(--color-border-default);
        border-radius: var(--radius-md);
        box-shadow: {elevation.levels['surface']['box-shadow']};
        z-index: {elevation.levels['surface']['z-index']};
        transition: transform var(--motion-hover), box-shadow var(--motion-hover), border-color var(--motion-hover);
    }}
    
    .surface-raised {{
        background-color: var(--color-bg-surface-raised);
        box-shadow: {elevation.levels['raised']['box-shadow']};
        z-index: {elevation.levels['raised']['z-index']};
    }}
    
    /* Interactive Card Override */
    .surface-interactive:hover {{
        border-color: var(--color-border-hover);
        transform: translateY(-2px);
        box-shadow: {elevation.levels['raised']['box-shadow']};
    }}

    /* =========================================================================
       4. ACCESSIBILITY & NATIVE OVERRIDES
       ========================================================================= */
       
    /* Minimum touch target (44x44) & Focus Rings */
    *:focus-visible {{
        outline: 2px solid var(--color-accent-primary) !important;
        outline-offset: 2px !important;
    }}
    
    .stButton > button {{
        min-height: 44px; /* Touch target */
        background-color: var(--color-bg-surface-raised);
        color: var(--color-text-primary);
        border: 1px solid var(--color-border-default);
        border-radius: var(--radius-md);
        font-weight: 500;
        transition: all var(--motion-hover);
        width: 100%;
    }}
    .stButton > button:hover {{
        border-color: var(--color-border-hover);
        background-color: var(--color-bg-surface-raised);
    }}
    
    /* Primary CTA */
    [data-testid="stFormSubmitButton"] > button {{
        background-color: var(--color-accent-primary);
        color: #ffffff !important;
        border: none;
    }}
    [data-testid="stFormSubmitButton"] > button:hover {{
        background-color: var(--color-accent-hover);
    }}

    /* Inputs */
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {{
        min-height: 44px;
        background-color: var(--color-bg-surface) !important;
        border: 1px solid var(--color-border-default) !important;
        color: var(--color-text-primary) !important;
        border-radius: var(--radius-md);
        transition: border-color var(--motion-focus), box-shadow var(--motion-focus);
    }}
    
    .stTextInput > div > div > input:focus, 
    .stSelectbox > div > div > div:focus-within,
    .stTextArea > div > div > textarea:focus {{
        border-color: var(--color-accent-primary) !important;
        box-shadow: 0 0 0 2px var(--color-accent-subtle) !important;
    }}

    /* Badges */
    .badge {{
        display: inline-flex;
        align-items: center;
        padding: var(--space-1) var(--space-2);
        border-radius: var(--radius-full);
        font-size: 0.75rem;
        font-weight: 500;
    }}
    .badge-success {{ background: var(--color-status-success-subtle); color: var(--color-status-success); }}
    .badge-warning {{ background: var(--color-status-warning-subtle); color: var(--color-status-warning); }}
    .badge-error {{ background: var(--color-status-error-subtle); color: var(--color-status-error); }}
    .badge-info {{ background: var(--color-status-info-subtle); color: var(--color-status-info); }}

</style>
"""
    return css

def inject_styles():
    """Injects the global CSS design system into the Streamlit app."""
    st.markdown(get_global_css(), unsafe_allow_html=True)
