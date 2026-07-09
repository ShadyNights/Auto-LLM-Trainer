import streamlit as st
from src.ui.design import tokens, themes, typography, elevation, motion

    # Tailwind script injection
    html = """
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "inverse-primary": "#006877",
                        "outline": "#859397",
                        "surface-container-highest": "#2d3449",
                        "on-tertiary-fixed": "#251a00",
                        "on-secondary": "#263143",
                        "on-tertiary": "#3f2e00",
                        "surface-container-low": "#131b2e",
                        "secondary-container": "#3e495d",
                        "tertiary-container": "#fec42e",
                        "primary-fixed": "#a5eeff",
                        "surface-tint": "#00daf8",
                        "surface-container-high": "#222a3d",
                        "inverse-on-surface": "#283044",
                        "inverse-surface": "#dae2fd",
                        "on-surface": "#dae2fd",
                        "on-tertiary-fixed-variant": "#5b4300",
                        "tertiary-fixed": "#ffdf9d",
                        "surface-variant": "#2d3449",
                        "surface-container": "#171f33",
                        "on-background": "#dae2fd",
                        "tertiary": "#ffe6b6",
                        "primary": "#baf2ff",
                        "surface-bright": "#31394d",
                        "secondary-fixed-dim": "#bcc7de",
                        "on-tertiary-container": "#6f5200",
                        "on-primary-container": "#005f6d",
                        "on-error": "#690005",
                        "on-error-container": "#ffdad6",
                        "surface-dim": "#0b1326",
                        "error-container": "#93000a",
                        "on-primary-fixed": "#001f25",
                        "secondary-fixed": "#d8e3fb",
                        "primary-container": "#00e0ff",
                        "outline-variant": "#3b494c",
                        "on-surface-variant": "#bac9cd",
                        "on-secondary-container": "#aeb9d0",
                        "tertiary-fixed-dim": "#f7be27",
                        "surface": "#0b1326",
                        "on-primary-fixed-variant": "#004e5a",
                        "on-secondary-fixed-variant": "#3c475a",
                        "background": "#0b1326",
                        "on-secondary-fixed": "#111c2d",
                        "on-primary": "#00363f",
                        "primary-fixed-dim": "#00daf8",
                        "secondary": "#bcc7de",
                        "surface-container-lowest": "#060e20",
                        "error": "#ffb4ab"
                    },
                    "borderRadius": {
                        "DEFAULT": "0.125rem",
                        "lg": "0.25rem",
                        "xl": "0.5rem",
                        "full": "0.75rem"
                    },
                    "spacing": {
                        "xs": "0.25rem",
                        "lg": "1.5rem",
                        "md": "1rem",
                        "container-max": "1440px",
                        "xl": "2.5rem",
                        "sm": "0.5rem",
                        "base": "4px"
                    },
                    "fontFamily": {
                        "body-md": ["Geist"],
                        "display-lg-mobile": ["Space Grotesk"],
                        "display-lg": ["Space Grotesk"],
                        "headline-md": ["Geist"],
                        "label-xs": ["Geist"],
                        "code-sm": ["JetBrains Mono"]
                    },
                    "fontSize": {
                        "body-md": ["16px", { "lineHeight": "1.6", "fontWeight": "400" }],
                        "display-lg-mobile": ["32px", { "lineHeight": "1.2", "fontWeight": "700" }],
                        "display-lg": ["48px", { "lineHeight": "1.1", "letterSpacing": "-0.02em", "fontWeight": "700" }],
                        "headline-md": ["24px", { "lineHeight": "1.4", "fontWeight": "600" }],
                        "label-xs": ["12px", { "lineHeight": "1.0", "letterSpacing": "0.05em", "fontWeight": "500" }],
                        "code-sm": ["13px", { "lineHeight": "1.5", "fontWeight": "400" }]
                    }
                }
            }
        };
    </script>
    <style>
        .ai-pulse {
            animation: pulse-border 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        @keyframes pulse-border {
            0%, 100% { border-color: rgba(0, 224, 255, 0.2); box-shadow: 0 0 8px rgba(0, 224, 255, 0.05); }
            50% { border-color: rgba(0, 224, 255, 0.6); box-shadow: 0 0 12px rgba(0, 224, 255, 0.15); }
        }
        .blinking-cursor::after {
            content: '█';
            animation: blink 1s step-end infinite;
            color: #00daf8;
            margin-left: 4px;
        }
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        .skeleton-pulse {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: .5; }
        }
    </style>
    """
    st.components.v1.html(html, height=0)
    
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
