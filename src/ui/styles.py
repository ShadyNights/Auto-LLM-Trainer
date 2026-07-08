import streamlit as st

def get_global_css() -> str:
    return """
<style>
    /* =========================================================================
       1. TOKENS
       ========================================================================= */
    :root {
        /* Colors: Surfaces & Backgrounds */
        --bg-base: #0d1117;
        --bg-surface: #161b22;
        --bg-surface-raised: #21262d;
        --bg-sidebar: #0f1218;

        /* Colors: Typography */
        --text-primary: #f0f6fc;
        --text-secondary: #8b949e;
        --text-muted: #6e7681;

        /* Colors: Accents (Blue / Indigo) */
        --accent-primary: #58a6ff;
        --accent-hover: #79c0ff;
        --accent-active: #3182ce;
        --accent-subtle: rgba(88, 166, 255, 0.15);

        /* Colors: Semantic Status */
        --status-success: #238636;
        --status-success-subtle: rgba(35, 134, 54, 0.15);
        --status-warning: #d29922;
        --status-warning-subtle: rgba(210, 153, 34, 0.15);
        --status-error: #f85149;
        --status-error-subtle: rgba(248, 81, 73, 0.15);
        --status-info: #58a6ff;

        /* Borders & Shadows */
        --border-color: rgba(240, 246, 252, 0.1);
        --border-hover: rgba(240, 246, 252, 0.2);
        
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.4);
        --shadow-md: 0 4px 8px rgba(0,0,0,0.5);
        --shadow-lg: 0 12px 24px rgba(0,0,0,0.6);

        /* Radius */
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;

        /* Spacing System (8pt Grid) */
        --spacing-1: 4px;
        --spacing-2: 8px;
        --spacing-3: 12px;
        --spacing-4: 16px;
        --spacing-5: 20px;
        --spacing-6: 24px;
        --spacing-8: 32px;
        --spacing-10: 40px;
        --spacing-12: 48px;
        --spacing-16: 64px;

        /* Animations & Transitions */
        --transition-100: 100ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-150: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-200: 200ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-250: 250ms cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Accessibility: Reduced Motion */
    @media (prefers-reduced-motion: reduce) {
        *, ::before, ::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
    }

    /* =========================================================================
       2. BASE & TYPOGRAPHY
       ========================================================================= */
    .stApp {
        background-color: var(--bg-base);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        margin-top: 0;
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    p {
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* =========================================================================
       3. NATIVE STREAMLIT OVERRIDES (Stable Selectors)
       ========================================================================= */
    
    /* Focus Rings (Accessibility) */
    *:focus-visible {
        outline: 2px solid var(--accent-primary) !important;
        outline-offset: 2px !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar);
        border-right: 1px solid var(--border-color);
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-muted);
        margin-top: var(--spacing-4);
        margin-bottom: var(--spacing-2);
    }

    /* Buttons */
    .stButton > button {
        background-color: var(--bg-surface-raised);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: var(--spacing-2) var(--spacing-4);
        font-weight: 500;
        transition: all var(--transition-150);
        width: 100%;
        box-shadow: var(--shadow-sm);
    }
    .stButton > button:hover {
        border-color: var(--border-hover);
        background-color: var(--bg-surface-raised);
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: none;
        background-color: var(--bg-surface);
    }
    /* Primary Submit Form Button Exception */
    [data-testid="stFormSubmitButton"] > button {
        background-color: var(--accent-primary);
        color: #ffffff !important;
        border: none;
    }
    [data-testid="stFormSubmitButton"] > button:hover {
        background-color: var(--accent-hover);
    }
    [data-testid="stFormSubmitButton"] > button:active {
        background-color: var(--accent-active);
    }

    /* Inputs (Text, Select, Number) */
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        border-radius: var(--radius-md);
        padding: var(--spacing-2) var(--spacing-3);
        transition: border-color var(--transition-150), box-shadow var(--transition-150);
    }
    .stTextInput > div > div > input:focus, 
    .stSelectbox > div > div > div:focus-within,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 2px var(--accent-subtle) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: var(--spacing-4);
        border-bottom: 1px solid var(--border-color);
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: var(--text-secondary);
        font-weight: 500;
        padding-top: var(--spacing-2);
        padding-bottom: var(--spacing-2);
        border-radius: var(--radius-sm) var(--radius-sm) 0 0;
        transition: color var(--transition-150);
    }
    .stTabs [aria-selected="true"] {
        color: var(--text-primary) !important;
        border-bottom: 2px solid var(--accent-primary);
    }
    .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
        color: var(--text-primary);
    }

    /* Forms */
    [data-testid="stForm"] {
        background-color: var(--bg-surface);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: var(--spacing-6);
        box-shadow: var(--shadow-sm);
    }

    /* Expanders */
    [data-testid="stExpander"] {
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        background-color: var(--bg-surface);
    }
    [data-testid="stExpander"] summary {
        color: var(--text-primary);
        font-weight: 500;
    }

    /* Horizontal Rules */
    hr {
        border-top: 1px solid var(--border-color) !important;
        margin: var(--spacing-4) 0;
    }

    /* =========================================================================
       4. UTILITY CLASSES & CUSTOM COMPONENTS
       ========================================================================= */

    /* Cards */
    .card {
        background-color: var(--bg-surface);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: var(--spacing-4);
        margin-bottom: var(--spacing-4);
    }
    .card--raised {
        box-shadow: var(--shadow-sm);
        transition: transform var(--transition-150), box-shadow var(--transition-150);
    }
    .card--raised:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }

    /* Typography Utilities */
    .text-primary { color: var(--text-primary); }
    .text-secondary { color: var(--text-secondary); }
    .text-muted { color: var(--text-muted); font-size: 0.85rem; }
    .text-accent { color: var(--accent-primary); }

    /* Layout Utilities */
    .flex { display: flex; }
    .flex-col { flex-direction: column; }
    .items-center { align-items: center; }
    .justify-between { justify-content: space-between; }
    .justify-center { justify-content: center; }
    .gap-2 { gap: var(--spacing-2); }
    .gap-4 { gap: var(--spacing-4); }

    /* Hero Section */
    .hero {
        padding: var(--spacing-6) 0;
        margin-bottom: var(--spacing-4);
    }
    .hero h1 {
        font-size: 2rem;
        margin-bottom: var(--spacing-2);
        color: var(--text-primary);
    }
    .hero p {
        font-size: 1.1rem;
        color: var(--text-secondary);
        max-width: 600px;
    }

    /* Metric Cards */
    .metric {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-2);
    }
    .metric-title {
        font-size: 0.85rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }
    .metric-value {
        font-size: 1.75rem;
        font-weight: 600;
        color: var(--text-primary);
        line-height: 1;
    }
    .metric-footer {
        display: flex;
        align-items: center;
        gap: var(--spacing-2);
        font-size: 0.8rem;
    }

    /* Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
        line-height: 1.2;
    }
    .badge--success { background: var(--status-success-subtle); color: var(--status-success); }
    .badge--warning { background: var(--status-warning-subtle); color: var(--status-warning); }
    .badge--error { background: var(--status-error-subtle); color: var(--status-error); }
    .badge--info { background: var(--accent-subtle); color: var(--accent-primary); }
    .badge--neutral { background: rgba(110, 118, 129, 0.15); color: var(--text-secondary); }

    /* Empty States */
    .empty-state {
        text-align: center;
        padding: var(--spacing-10);
        background-color: transparent;
        border: 1px dashed var(--border-color);
        border-radius: var(--radius-lg);
    }
    .empty-state-icon {
        font-size: 2.5rem;
        margin-bottom: var(--spacing-4);
        color: var(--text-muted);
    }
    .empty-state h3 {
        margin-bottom: var(--spacing-2);
    }

    /* Skeleton Loading */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    .skeleton {
        animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        background-color: var(--bg-surface-raised);
        border-radius: var(--radius-sm);
        margin-bottom: var(--spacing-2);
    }
    .skeleton-title { height: 28px; width: 40%; margin-bottom: var(--spacing-4); }
    .skeleton-text { height: 16px; width: 100%; }
    .skeleton-text-short { width: 60%; }

</style>
"""

def inject_styles():
    """Injects the global CSS design system into the Streamlit app."""
    st.markdown(get_global_css(), unsafe_allow_html=True)
