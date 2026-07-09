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
        if key != "loading":
            css_vars.append(f"        --motion-{key}: {value};")

    return "\n".join(css_vars)


def get_global_css() -> str:
    """Generates the unified Design System CSS with Aggressive Native Overrides."""
    
    css = f"""
<style>
    /* =========================================================================
       1. COMPILED DESIGN TOKENS
       ========================================================================= */
       
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
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
       2. TYPOGRAPHY (Native Streamlit Override)
       ========================================================================= */
       
    /* Force Geist onto all generic elements */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label, .stApp input, .stApp textarea, .stApp button {{
        font-family: {typography.levels['body']['font-family']} !important;
    }}
    
    /* Apply Typography Levels */
    .type-display, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {{
        font-family: {typography.levels['display']['font-family']} !important;
        font-size: {typography.levels['display']['font-size']} !important;
        font-weight: {typography.levels['display']['font-weight']} !important;
        line-height: {typography.levels['display']['line-height']} !important;
        letter-spacing: {typography.levels['display']['letter-spacing']} !important;
        color: var(--color-text-primary);
    }}
    
    h1, .type-heading {{
        font-family: {typography.levels['heading']['font-family']} !important;
        font-size: {typography.levels['heading']['font-size']} !important;
        font-weight: {typography.levels['heading']['font-weight']} !important;
        line-height: {typography.levels['heading']['line-height']} !important;
        letter-spacing: {typography.levels['heading']['letter-spacing']} !important;
        color: var(--color-text-primary);
    }}
    h2, h3, .type-title {{
        font-family: {typography.levels['title']['font-family']} !important;
        font-size: {typography.levels['title']['font-size']} !important;
        font-weight: {typography.levels['title']['font-weight']} !important;
        line-height: {typography.levels['title']['line-height']} !important;
        color: var(--color-text-primary);
    }}
    p, .type-body {{
        font-family: {typography.levels['body']['font-family']} !important;
        font-size: {typography.levels['body']['font-size']} !important;
        font-weight: {typography.levels['body']['font-weight']} !important;
        line-height: {typography.levels['body']['line-height']} !important;
        color: var(--color-text-secondary);
    }}
    small, .type-caption {{
        font-family: {typography.levels['caption']['font-family']} !important;
        font-size: {typography.levels['caption']['font-size']} !important;
        font-weight: {typography.levels['caption']['font-weight']} !important;
        text-transform: {typography.levels['caption']['text-transform']} !important;
        letter-spacing: {typography.levels['caption']['letter-spacing']} !important;
        color: var(--color-text-muted);
    }}

    /* =========================================================================
       3. NATIVE COMPONENT OVERRIDES (Tailwind Sync)
       ========================================================================= */
       
    /* Hide top header spacing */
    [data-testid="stHeader"] {{
        display: none !important;
    }}
    
    /* Layout Container (Remove native padding for edge-to-edge Tailwind) */
    .block-container {{
        padding-top: var(--space-8) !important;
        padding-left: var(--space-6) !important;
        padding-right: var(--space-6) !important;
        max-width: 1440px !important;
    }}
       
    /* Sidebar Strict Override */
    [data-testid="stSidebar"] {{
        background-color: var(--color-bg-surface-lowest) !important;
        border-right: 1px solid var(--color-border-default) !important;
        width: 288px !important; /* 72 Tailwind rem */
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        padding: var(--space-8) var(--space-4) !important;
    }}
    
    /* Inputs Override (Tailwind text inputs) */
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background-color: var(--color-bg-surface-low) !important;
        border: 1px solid var(--color-border-default) !important;
        color: var(--color-text-primary) !important;
        border-radius: var(--radius-md) !important;
        min-height: 44px !important;
        font-size: 16px !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        transition: border-color var(--motion-focus), box-shadow var(--motion-focus) !important;
    }}
    
    /* Input Focus Rings (Cyan Primary Container) */
    .stTextInput > div > div > input:focus, 
    .stSelectbox > div > div > div:focus-within,
    .stTextArea > div > div > textarea:focus {{
        border-color: var(--color-accent-primary) !important;
        box-shadow: 0 0 0 1px var(--color-accent-primary) !important;
    }}
    
    /* Button Override */
    .stButton > button {{
        background-color: var(--color-bg-surface-high) !important;
        border: 1px solid var(--color-border-default) !important;
        color: var(--color-text-primary) !important;
        border-radius: var(--radius-md) !important;
        font-weight: 500 !important;
        min-height: 40px !important;
        transition: all var(--motion-hover) !important;
    }}
    
    .stButton > button:hover {{
        background-color: var(--color-bg-surface-highest) !important;
        border-color: var(--color-border-hover) !important;
    }}
    
    /* Primary CTA Button Override (Generate Premium Itinerary) */
    [data-testid="stFormSubmitButton"] > button,
    .stButton > button[data-baseweb="button"]:has(p:contains("New Itinerary")) {{
        background-color: var(--color-accent-primary) !important;
        color: var(--color-text-on-primary) !important;
        border: none !important;
        font-weight: 700 !important;
        box-shadow: 0 0 15px rgba(0, 224, 255, 0.2) !important;
    }}
    
    [data-testid="stFormSubmitButton"] > button:hover,
    .stButton > button[data-baseweb="button"]:has(p:contains("New Itinerary")):hover {{
        background-color: var(--color-accent-active) !important;
        box-shadow: 0 0 20px rgba(0, 224, 255, 0.4) !important;
        transform: translateY(-1px);
    }}

    /* Custom Primitives */
    .surface {{
        background-color: var(--color-bg-surface-high);
        border: 1px solid var(--color-border-default);
        border-radius: var(--radius-lg);
        box-shadow: {elevation.levels['surface']['box-shadow']};
    }}
    
    .surface-interactive:hover {{
        border-color: var(--color-border-hover);
        transform: translateY(-2px);
        box-shadow: {elevation.levels['raised']['box-shadow']};
    }}

    .badge {{
        display: inline-flex;
        align-items: center;
        padding: var(--space-1) var(--space-2);
        border-radius: var(--radius-full);
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
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
