import streamlit as st
import json

def inject_styles():
    """Injects the global CSS design system into the Streamlit app using exact explicit CSS rules."""
    
    css = """
<style>
    /* ==========================================================================
       TAILWIND CSS EXPLICIT MAPPING
       We map the exact Tailwind classes used in the HTML to raw CSS to bypass
       Streamlit's JavaScript sanitization restrictions.
       ========================================================================== */
       
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    :root {
        --color-background: #0B1326;
        --color-on-background: #dae2fd;
        --color-surface-container-lowest: #060e20;
        --color-surface-container-low: #131b2e;
        --color-surface-container: #171f33;
        --color-surface-container-high: #222a3d;
        --color-outline-variant: #3b494c;
        --color-surface-variant: #2d3449;
        --color-primary-container: #00e0ff;
        --color-on-primary-container: #005f6d;
        --color-primary-fixed: #a5eeff;
        --color-primary-fixed-dim: #00daf8;
        --color-on-surface: #dae2fd;
        --color-on-surface-variant: #bac9cd;
    }
    
    body {
        font-family: 'Geist', sans-serif !important;
        background-color: var(--color-background) !important;
        color: var(--color-on-background) !important;
    }
    
    /* Hide Streamlit Native Elements */
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; background-color: var(--color-background); }
    
    /* Layout */
    .flex { display: flex; }
    .flex-col { flex-direction: column; }
    .items-center { align-items: center; }
    .items-end { align-items: flex-end; }
    .justify-center { justify-content: center; }
    .justify-between { justify-content: space-between; }
    .justify-around { justify-content: space-around; }
    .shrink-0 { flex-shrink: 0; }
    .flex-1 { flex: 1 1 0%; }
    .flex-wrap { flex-wrap: wrap; }
    
    .grid { display: grid; }
    .grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
    @media (min-width: 768px) { .md\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
    @media (min-width: 768px) { .md\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
    @media (min-width: 1024px) { .lg\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
    .lg\:col-span-2 { grid-column: span 2 / span 2; }
    
    .hidden { display: none; }
    @media (min-width: 768px) { .md\:flex { display: flex; } .md\:hidden { display: none; } }
    
    /* Dimensions */
    .h-screen { height: 100vh; }
    .w-full { width: 100%; }
    .h-full { height: 100%; }
    .w-72 { width: 18rem; /* 288px */ }
    .w-12 { width: 3rem; }
    .h-12 { height: 3rem; }
    .w-10 { width: 2.5rem; }
    .h-10 { height: 2.5rem; }
    .h-16 { height: 4rem; }
    .h-48 { height: 12rem; }
    .h-4 { height: 1rem; }
    .w-4 { width: 1rem; }
    .h-2\.5 { height: 0.625rem; }
    .w-2\.5 { width: 0.625rem; }
    .h-6 { height: 1.5rem; }
    .h-5 { height: 1.25rem; }
    .w-1\/3 { width: 33.333333%; }
    .w-1\/2 { width: 50%; }
    .w-1\/4 { width: 25%; }
    .w-1\/6 { width: 16.666667%; }
    
    .max-w-2xl { max-w: 42rem; }
    .max-w-\[1280px\] { max-width: 1280px; }
    .mx-auto { margin-left: auto; margin-right: auto; }
    
    /* Spacing mapped to User HTML */
    .gap-\[4px\] { gap: 4px; }
    .gap-\[8px\] { gap: 8px; }
    .gap-[8px] { gap: 8px; }
    .gap-\[16px\] { gap: 16px; }
    .gap-\[24px\] { gap: 24px; }
    
    .p-2 { padding: 0.5rem; }
    .p-\[16px\] { padding: 16px; }
    .p-[16px] { padding: 16px; }
    .p-\[24px\] { padding: 24px; }
    .px-\[8px\] { padding-left: 8px; padding-right: 8px; }
    .px-[8px] { padding-left: 8px; padding-right: 8px; }
    .px-\[16px\] { padding-left: 16px; padding-right: 16px; }
    .px-[16px] { padding-left: 16px; padding-right: 16px; }
    .px-\[24px\] { padding-left: 24px; padding-right: 24px; }
    .px-[24px] { padding-left: 24px; padding-right: 24px; }
    .py-0\.5 { padding-top: 0.125rem; padding-bottom: 0.125rem; }
    .py-\[8px\] { padding-top: 8px; padding-bottom: 8px; }
    .py-[8px] { padding-top: 8px; padding-bottom: 8px; }
    .py-\[16px\] { padding-top: 16px; padding-bottom: 16px; }
    .py-\[32px\] { padding-top: 32px; padding-bottom: 32px; }
    .pt-\[8px\] { padding-top: 8px; }
    .pt-[8px] { padding-top: 8px; }
    .pt-\[16px\] { padding-top: 16px; }
    .pt-\[32px\] { padding-top: 32px; }
    
    .pl-\[32px\] { padding-left: 32px; }
    
    .mb-1 { margin-bottom: 0.25rem; }
    .mb-2 { margin-bottom: 0.5rem; }
    .mb-4 { margin-bottom: 1rem; }
    .mb-6 { margin-bottom: 1.5rem; }
    .mb-8 { margin-bottom: 2rem; }
    
    .mb-\[8px\] { margin-bottom: 8px; }
    .mb-\[16px\] { margin-bottom: 16px; }
    .mb-[16px] { margin-bottom: 16px; }
    .mb-\[24px\] { margin-bottom: 24px; }
    .mt-\[16px\] { margin-top: 16px; }
    .mt-[16px] { margin-top: 16px; }
    .mt-1 { margin-top: 0.25rem; }
    .mt-2 { margin-top: 0.5rem; }
    .mt-4 { margin-top: 1rem; }
    .mt-auto { margin-top: auto; }
    
    .space-y-\[8px\] > :not([hidden]) ~ :not([hidden]) { margin-top: 8px; }
    .space-y-\[16px\] > :not([hidden]) ~ :not([hidden]) { margin-top: 16px; }
    .space-y-[16px] > :not([hidden]) ~ :not([hidden]) { margin-top: 16px; }
    .space-y-\[24px\] > :not([hidden]) ~ :not([hidden]) { margin-top: 24px; }
    .space-y-[24px] > :not([hidden]) ~ :not([hidden]) { margin-top: 24px; }
    .space-y-\[32px\] > :not([hidden]) ~ :not([hidden]) { margin-top: 32px; }
    .space-y-[32px] > :not([hidden]) ~ :not([hidden]) { margin-top: 32px; }
    .space-y-\[40px\] > :not([hidden]) ~ :not([hidden]) { margin-top: 40px; }
    
    /* Layout utility */
    .overflow-hidden { overflow: hidden; }
    .overflow-y-auto { overflow-y: auto; }
    .relative { position: relative; }
    .absolute { position: absolute; }
    .sticky { position: sticky; }
    .top-0 { top: 0px; }
    .bottom-\[16px\] { bottom: 16px; }
    .left-\[16px\] { left: 16px; }
    .right-\[16px\] { right: 16px; }
    .-left-\[9px\] { left: -9px; }
    .inset-0 { top: 0px; right: 0px; bottom: 0px; left: 0px; }
    .z-10 { z-index: 10; }
    
    /* Typography */
    .font-display-lg-mobile { font-family: 'Space Grotesk', sans-serif; font-size: 32px; font-weight: 700; line-height: 1.2; }
    .text-display-lg-mobile { font-size: 32px; line-height: 1.2; }
    .font-display-lg { font-family: 'Space Grotesk', sans-serif; font-size: 48px; font-weight: 700; line-height: 1.1; letter-spacing: -0.02em; }
    .text-display-lg { font-size: 48px; line-height: 1.1; }
    .font-headline-md { font-family: 'Geist', sans-serif; font-size: 24px; font-weight: 600; line-height: 1.4; }
    .text-headline-md { font-size: 24px; line-height: 1.4; }
    .font-body-md { font-family: 'Geist', sans-serif; font-size: 16px; font-weight: 400; line-height: 1.6; }
    .text-body-md { font-size: 16px; line-height: 1.6; }
    .font-label-xs { font-family: 'Geist', sans-serif; font-size: 12px; font-weight: 500; line-height: 1.0; letter-spacing: 0.05em; }
    .text-label-xs { font-size: 12px; line-height: 1.0; }
    .font-code-sm { font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 400; line-height: 1.5; }
    .text-code-sm { font-size: 13px; line-height: 1.5; }
    
    .font-semibold { font-weight: 600; }
    .font-bold { font-weight: 700; }
    .font-medium { font-weight: 500; }
    .uppercase { text-transform: uppercase; }
    .tracking-tight { letter-spacing: -0.025em; }
    .tracking-wider { letter-spacing: 0.05em; }
    .truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .text-\[10px\] { font-size: 10px; }
    
    /* Colors */
    .bg-background { background-color: var(--color-background); }
    .text-on-background { color: var(--color-on-background); }
    .bg-surface-container-lowest { background-color: var(--color-surface-container-lowest); }
    .bg-surface-container-low { background-color: var(--color-surface-container-low); }
    .bg-surface-container { background-color: var(--color-surface-container); }
    .bg-surface-container-high { background-color: var(--color-surface-container-high); }
    .bg-primary-container { background-color: var(--color-primary-container); }
    .text-on-primary-container { color: var(--color-on-primary-container); }
    .text-primary-fixed-dim { color: var(--color-primary-fixed-dim); }
    .text-on-surface { color: var(--color-on-surface); }
    .text-on-surface-variant { color: var(--color-on-surface-variant); }
    .bg-surface-variant { background-color: var(--color-surface-variant); }
    
    .hover\:text-primary-fixed-dim:hover { color: var(--color-primary-fixed-dim); }
    .hover\:text-on-background:hover { color: var(--color-on-background); }
    .hover\:bg-surface-container:hover { background-color: var(--color-surface-container); }
    .hover\:bg-primary-fixed:hover { background-color: var(--color-primary-fixed); }
    .hover\:bg-surface-container-highest:hover { background-color: #2d3449; }
    
    .bg-background\/50 { background-color: rgba(11, 19, 38, 0.5); }
    
    /* Borders */
    .border { border-width: 1px; }
    .border-r { border-right-width: 1px; }
    .border-t { border-top-width: 1px; }
    .border-b { border-bottom-width: 1px; }
    .border-l { border-left-width: 1px; }
    
    .border-outline-variant { border-color: var(--color-outline-variant); }
    .border-surface-variant { border-color: var(--color-surface-variant); }
    .border-primary-fixed { border-color: var(--color-primary-fixed); }
    .border-primary-container { border-color: var(--color-primary-container); }
    
    .rounded-full { border-radius: 9999px; }
    .rounded-lg { border-radius: 0.5rem; }
    .rounded-t-lg { border-top-left-radius: 0.5rem; border-top-right-radius: 0.5rem; }
    .rounded-xl { border-radius: 0.75rem; }
    .rounded-md { border-radius: 0.375rem; }
    
    .ring-1 { box-shadow: var(--tw-ring-inset) 0 0 0 calc(1px + var(--tw-ring-offset-width)) var(--tw-ring-color); }
    .ring-4 { box-shadow: var(--tw-ring-inset) 0 0 0 calc(4px + var(--tw-ring-offset-width)) var(--tw-ring-color); }
    .ring-outline-variant { --tw-ring-color: var(--color-outline-variant); }
    .ring-background { --tw-ring-color: var(--color-background); }
    
    .shadow-sm { box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); }
    
    /* Images */
    .object-cover { object-fit: cover; }
    .bg-cover { background-size: cover; }
    .bg-center { background-position: center; }
    .opacity-40 { opacity: 0.4; }
    .opacity-70 { opacity: 0.7; }
    .mix-blend-overlay { mix-blend-mode: overlay; }
    .mix-blend-screen { mix-blend-mode: screen; }
    
    /* Animations */
    .transition-colors { transition-property: color, background-color, border-color, text-decoration-color, fill, stroke; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; }
    .duration-200 { transition-duration: 200ms; }
    .transition-transform { transition-property: transform; }
    .scale-95 { transform: scale(.95); }
    
    .animate-fade-in { animation: fadeIn 0.5s ease-in-out; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    
    /* Specific Custom Classes from HTML */
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
    
    /* Additional custom mappings from HTML */
    .text-\[11px\] { font-size: 11px; }
    .text-\[18px\] { font-size: 18px; }
    .text-\[32px\] { font-size: 32px; }
    .tracking-widest { letter-spacing: 0.1em; }
    
    .mt-xs { margin-top: 4px; }
    .mt-md { margin-top: 16px; }
    .pt-sm { padding-top: 8px; }
    .pt-md { padding-top: 16px; }
    .pb-xs { padding-bottom: 4px; }
    
    .shadow-\[0_0_8px_rgba\(0\,224\,255\,0\.6\)\] { box-shadow: 0 0 8px rgba(0,224,255,0.6); }
    .shadow-\[0_0_10px_rgba\(0\,224\,255\,0\.15\)\] { box-shadow: 0 0 10px rgba(0,224,255,0.15); }
    .shadow-\[0_0_15px_rgba\(0\,224\,255\,0\.2\)\] { box-shadow: 0 0 15px rgba(0,224,255,0.2); }
    .hover\:shadow-\[0_0_20px_rgba\(0\,224\,255\,0\.4\)\]:hover { box-shadow: 0 0 20px rgba(0,224,255,0.4); }
    .hover\:shadow-md:hover { box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }
    
    .animate-ping { animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite; }
    @keyframes ping {
        75%, 100% { transform: scale(2); opacity: 0; }
    }
    
    .group:hover .group-hover\:opacity-40 { opacity: 0.4; }
    
    /* Input Styling Override */
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: var(--color-surface-container-low) !important;
        border: 1px solid var(--color-outline-variant) !important;
        color: var(--color-on-surface) !important;
        border-radius: 0.5rem !important;
        min-height: 44px !important;
        font-family: 'Geist', sans-serif !important;
        font-size: 16px !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--color-primary-container) !important;
        box-shadow: 0 0 0 1px var(--color-primary-container) !important;
    }
</style>
"""
    st.markdown(css, unsafe_allow_html=True)
