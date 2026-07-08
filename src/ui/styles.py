import streamlit as st

def get_global_css() -> str:
    return """
<style>
    /* Design Tokens */
    :root {
        --bg-primary: #0f1115;
        --bg-secondary: #161b22;
        --surface: #1c2128;
        --border: #30363d;
        --border-hover: #8b949e;

        --text-primary: #f0f6fc;
        --text-secondary: #8b949e;

        --accent-start: #667eea;
        --accent-end: #764ba2;
        --accent-hover: #8a96ff;

        --success: #3fb950;
        --warning: #d29922;
        --error: #f85149;
        --info: #3182ce;
        --neutral: #6e7681;

        --spacing-1: 4px;
        --spacing-2: 8px;
        --spacing-3: 12px;
        --spacing-4: 16px;
        --spacing-6: 24px;
        --spacing-8: 32px;
        --spacing-12: 48px;
        --spacing-16: 64px;

        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 18px;

        --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
        --shadow-md: 0 4px 6px rgba(0,0,0,0.4);
        --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.5);
        
        --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Base Body Reset */
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
        font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Typography overrides for main content */
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: var(--text-primary);
    }
    
    p {
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* Sidebar Overrides */
    [data-testid="stSidebar"] {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border);
        padding: var(--spacing-4);
    }
    [data-testid="stSidebar"] .css-1d391kg {
        background-color: transparent;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-start) 0%, var(--accent-end) 100%);
        color: #ffffff !important;
        border: none;
        border-radius: var(--radius-sm);
        padding: var(--spacing-2) var(--spacing-4);
        font-weight: 600;
        box-shadow: var(--shadow-sm);
        transition: all var(--transition-base);
        width: 100%;
    }
    .stButton > button:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
        background: linear-gradient(135deg, var(--accent-hover) 0%, var(--accent-end) 100%);
        color: #ffffff !important;
        border: none;
    }
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: none;
    }
    .stButton > button:focus:not(:focus-visible) {
        color: #ffffff !important;
    }

    /* Inputs */
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > div {
        background-color: var(--bg-primary) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-primary) !important;
        border-radius: var(--radius-sm);
        transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
        padding: var(--spacing-2) var(--spacing-3);
    }
    .stTextInput > div > div > input:focus, 
    .stSelectbox > div > div > div:focus-within {
        border-color: var(--accent-start) !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    .stSlider > div > div {
        /* Minimal style adjustments for slider if needed */
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: var(--spacing-4);
        border-bottom: 1px solid var(--border);
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: var(--radius-sm) var(--radius-sm) 0 0;
        color: var(--text-secondary);
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        color: var(--text-primary) !important;
        border-bottom: 2px solid var(--accent-start);
    }

    /* Forms */
    [data-testid="stForm"] {
        background-color: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: var(--spacing-6);
        box-shadow: var(--shadow-sm);
    }

    /* Dividers */
    hr {
        border-color: var(--border) !important;
        margin: var(--spacing-6) 0;
    }

    /* Component Library CSS */
    
    .ui-hero {
        text-align: center;
        padding: var(--spacing-12) var(--spacing-4);
        background: linear-gradient(180deg, var(--surface) 0%, transparent 100%);
        border-radius: var(--radius-lg);
        margin-bottom: var(--spacing-8);
        border: 1px solid var(--border);
    }
    .ui-hero h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: var(--spacing-2);
        background: linear-gradient(135deg, #ffffff 0%, var(--text-secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .ui-hero p {
        font-size: 1.1rem;
        color: var(--text-secondary);
        max-width: 600px;
        margin: 0 auto;
    }

    .ui-card {
        background-color: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: var(--spacing-4);
        margin-bottom: var(--spacing-4);
        box-shadow: var(--shadow-sm);
        transition: transform var(--transition-fast), box-shadow var(--transition-fast);
    }
    .ui-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    .ui-metric {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-1);
    }
    .ui-metric-header {
        display: flex;
        align-items: center;
        gap: var(--spacing-2);
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-weight: 500;
    }
    .ui-metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    .ui-metric-footer {
        display: flex;
        align-items: center;
        gap: var(--spacing-2);
        font-size: 0.8rem;
    }
    
    .ui-badge {
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .ui-badge.success { background: rgba(63, 185, 80, 0.1); color: var(--success); border: 1px solid rgba(63, 185, 80, 0.2); }
    .ui-badge.warning { background: rgba(210, 153, 34, 0.1); color: var(--warning); border: 1px solid rgba(210, 153, 34, 0.2); }
    .ui-badge.error { background: rgba(248, 81, 73, 0.1); color: var(--error); border: 1px solid rgba(248, 81, 73, 0.2); }
    .ui-badge.info { background: rgba(49, 130, 206, 0.1); color: var(--info); border: 1px solid rgba(49, 130, 206, 0.2); }
    .ui-badge.neutral { background: rgba(110, 118, 129, 0.1); color: var(--text-secondary); border: 1px solid rgba(110, 118, 129, 0.2); }

    .ui-empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: var(--spacing-12);
        background-color: var(--surface);
        border: 1px dashed var(--border);
        border-radius: var(--radius-md);
        text-align: center;
        color: var(--text-secondary);
    }
    .ui-empty-state h3 {
        color: var(--text-primary);
        margin: var(--spacing-4) 0 var(--spacing-2) 0;
    }

    /* Skeleton Loading Animation */
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    .ui-skeleton {
        animation: shimmer 2s infinite linear;
        background: linear-gradient(to right, var(--surface) 4%, var(--border) 25%, var(--surface) 36%);
        background-size: 1000px 100%;
        border-radius: var(--radius-sm);
        margin-bottom: var(--spacing-2);
    }
    .ui-skeleton.title { height: 32px; width: 60%; margin-bottom: var(--spacing-4); }
    .ui-skeleton.text { height: 16px; width: 100%; }
    .ui-skeleton.text.short { width: 80%; }
</style>
"""

def inject_styles():
    st.markdown(get_global_css(), unsafe_allow_html=True)
