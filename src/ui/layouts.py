import streamlit as st
from src.ui import components
from src.ui.icons import Icons
import textwrap

class BaseLayout:
    """Provides standard layout constraints and injections."""
    @staticmethod
    def setup_page(title: str):
        st.set_page_config(page_title=title, page_icon="✈️", layout="wide")
        
        # Inject custom Material Symbols font requirement to ensure icons load properly
        st.html("""
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
        <style>
            .material-symbols-outlined {
                font-family: 'Material Symbols Outlined' !important;
                font-weight: normal;
                font-style: normal;
                font-size: 24px;
                line-height: 1;
                letter-spacing: normal;
                text-transform: none;
                display: inline-block;
                white-space: nowrap;
                word-wrap: normal;
                direction: ltr;
                font-feature-settings: 'liga';
                -webkit-font-feature-settings: 'liga';
                -webkit-font-smoothing: antialiased;
            }
        </style>
        """)

class SidebarLayout:
    @staticmethod
    def render(session_id: str, warnings: list = None):
        with st.sidebar:
            st.html("""
            <div class="h-full flex flex-col pt-[32px] px-[16px]">
                <!-- Header -->
                <div class="flex items-center gap-[8px] px-[8px] mb-[16px]">
                    <span class="font-display-lg-mobile text-display-lg-mobile text-primary-fixed-dim tracking-tight">Traveler LLM</span>
                </div>
                
                <div class="flex items-center gap-[16px] px-[8px] mb-[24px]">
                    <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuDZvYxtOPSuoT8fq8jXUBiiXhZ-X9rqmlf4QguRuexgAIiXj3LzBAR5_5jejlXJFZ1MBujzaLbhBn9-cwjpNHAUS2-Z0qrUYV1iewStCRo58GW53xY2tVTeJcc4CepJxF2MPukPLmdB_SPFJhAYyiKMbCH2W4fQU2hzi8Co6VmuPizGxQ-B0hsJKQNvz-i7xzQrsoeiAklxqbIGbA7tfej0XD7vSfN6ko_ZYLbno-15lnRUk1-VkSOGIg" class="w-10 h-10 rounded-full object-cover border border-outline-variant" />
                    <div>
                        <div class="font-body-md text-body-md text-on-background font-semibold">Modern AI Professional</div>
                        <div class="font-code-sm text-code-sm text-on-surface-variant">Pro Account</div>
                    </div>
                </div>
            </div>
            """)
            
            st.button("New Itinerary", use_container_width=True, type="primary", icon=Icons.ADD)
            
            st.html("<div style='margin: var(--space-6) 0;'></div>")
            
            # Workspace Group
            st.html("<span class='px-md py-xs font-code-sm text-xs text-on-surface-variant uppercase tracking-wider block mb-2 px-[16px]'>Workspace</span>")
            st.html("""
            <div class="flex flex-col gap-[8px] px-[16px]">
                <a class="flex items-center gap-[16px] text-on-surface-variant hover:text-primary-fixed-dim px-[16px] py-[8px] rounded-lg transition-colors duration-200" href="#"><span class="material-symbols-outlined">dashboard</span><span class="font-body-md">Dashboard</span></a>
                <a class="flex items-center gap-[16px] bg-primary-container text-on-primary-container rounded-lg px-[16px] py-[8px] font-bold scale-95 transition-transform" href="#"><span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">auto_awesome</span><span class="font-body-md">Itinerary Planner</span></a>
                <a class="flex items-center gap-[16px] text-on-surface-variant hover:text-primary-fixed-dim px-[16px] py-[8px] rounded-lg transition-colors duration-200" href="#"><span class="material-symbols-outlined">map</span><span class="font-body-md">Active Trips</span></a>
            </div>
            """)
            
            st.html("<div style='margin: var(--space-6) 0;'></div>")
            
            # Operations Group
            st.html("<span class='px-md py-xs font-code-sm text-xs text-on-surface-variant uppercase tracking-wider block mb-2 px-[16px]'>Operations</span>")
            st.html("""
            <div class="flex flex-col gap-[8px] px-[16px]">
                <a class="flex items-center gap-[16px] text-on-surface-variant hover:text-primary-fixed-dim px-[16px] py-[8px] rounded-lg transition-colors duration-200" href="#"><span class="material-symbols-outlined">analytics</span><span class="font-body-md">System Health</span></a>
                <a class="flex items-center gap-[16px] text-on-surface-variant hover:text-primary-fixed-dim px-[16px] py-[8px] rounded-lg transition-colors duration-200" href="#"><span class="material-symbols-outlined">settings</span><span class="font-body-md">Configuration</span></a>
            </div>
            """)
            
            st.html("<div style='margin-top: 24px; border-top: 1px solid #3b494c; padding-top: 16px; margin-left: 16px; margin-right: 16px;'></div>")
            
            st.html("""
            <div class="flex flex-col gap-[8px] px-[16px]">
                <a class="flex items-center gap-[16px] text-on-surface-variant hover:text-primary-fixed-dim px-[16px] py-[8px] rounded-lg transition-colors duration-200" href="#"><span class="material-symbols-outlined">help</span><span class="font-code-sm">Help</span></a>
                <a class="flex items-center gap-[16px] text-on-surface-variant hover:text-primary-fixed-dim px-[16px] py-[8px] rounded-lg transition-colors duration-200" href="#"><span class="material-symbols-outlined">rate_review</span><span class="font-code-sm">Feedback</span></a>
            </div>
            """)

class DashboardLayout:
    @staticmethod
    def render_hero():
        html = """
        <section class="flex flex-col gap-md mb-8">
            <div class="flex flex-col gap-sm">
                <h1 class="font-display-lg text-display-lg-mobile md:text-display-lg text-on-surface mb-2">Traveler LLM</h1>
                <p class="font-body-md text-body-md text-on-surface-variant max-w-2xl">Automated itinerary curation powered by a Continuous Feedback Learning Pipeline.</p>
            </div>
            <div class="flex flex-wrap gap-sm mt-xs">
                <span class="inline-flex items-center gap-xs px-sm py-1 bg-surface-container border border-outline-variant rounded-full font-code-sm text-[11px] text-on-surface-variant">
                    <span class="w-1.5 h-1.5 rounded-full bg-primary-container"></span> Active Provider: Groq
                </span>
                <span class="inline-flex items-center gap-xs px-sm py-1 bg-surface-container border border-outline-variant rounded-full font-code-sm text-[11px] text-on-surface-variant">
                    Prompt: v1.2
                </span>
                <span class="inline-flex items-center gap-xs px-sm py-1 bg-surface-container border border-outline-variant rounded-full font-code-sm text-[11px] text-on-surface-variant">
                    Pipeline: Active
                </span>
            </div>
        </section>
        """
        st.html(html)
        
    @staticmethod
    def render_metrics(metrics: dict):
        total_conv = metrics.get('total_conversations', 0)
        rating = metrics.get('average_rating', 0)
        fails = metrics.get('generation_failures', 0)
        rating_str = f"{rating:.1f}" if rating else "N/A"
        
        html = f"""
        <section class="grid grid-cols-1 md:grid-cols-3 gap-md mb-8">
            <!-- Metric 1 -->
            <div class="bg-surface-container border border-outline-variant rounded-xl p-md flex flex-col gap-sm shadow-sm">
                <div class="flex items-center justify-between text-on-surface-variant mb-2">
                    <span class="font-label-xs text-label-xs uppercase tracking-wider">Total Conversations</span>
                    <span class="material-symbols-outlined" style="font-size: 18px;">forum</span>
                </div>
                <div class="font-code-sm text-[32px] font-bold text-on-surface leading-none mt-xs">{total_conv}</div>
                <div class="font-body-md text-sm text-on-surface-variant mb-4">All time interactions</div>
                <div class="flex items-center gap-xs text-primary-container font-code-sm text-xs mt-auto pt-sm border-t border-outline-variant/50">
                    <span class="material-symbols-outlined" style="font-size: 14px;">trending_up</span>
                    <span>+12% this week</span>
                </div>
            </div>
            <!-- Metric 2 -->
            <div class="bg-surface-container border border-outline-variant rounded-xl p-md flex flex-col gap-sm shadow-sm">
                <div class="flex items-center justify-between text-on-surface-variant mb-2">
                    <span class="font-label-xs text-label-xs uppercase tracking-wider">Avg Rating</span>
                    <span class="material-symbols-outlined" style="font-size: 18px;">star</span>
                </div>
                <div class="font-code-sm text-[32px] font-bold text-on-surface leading-none mt-xs">{rating_str}</div>
                <div class="font-body-md text-sm text-on-surface-variant mb-4">Based on user feedback</div>
                <div class="flex items-center gap-xs text-on-surface-variant font-code-sm text-xs mt-auto pt-sm border-t border-outline-variant/50">
                    <span>Consistent High Quality</span>
                </div>
            </div>
            <!-- Metric 3 -->
            <div class="bg-surface-container border border-outline-variant rounded-xl p-md flex flex-col gap-sm shadow-sm">
                <div class="flex items-center justify-between text-on-surface-variant mb-2">
                    <span class="font-label-xs text-label-xs uppercase tracking-wider">Gen Failures</span>
                    <span class="material-symbols-outlined" style="font-size: 18px;">bug_report</span>
                </div>
                <div class="font-code-sm text-[32px] font-bold text-on-surface leading-none mt-xs">{'Optimal' if fails == 0 else fails}</div>
                <div class="font-body-md text-sm text-on-surface-variant mb-4">Error rate within threshold</div>
                <div class="flex items-center gap-xs text-primary-container font-code-sm text-xs mt-auto pt-sm border-t border-outline-variant/50">
                    <span class="material-symbols-outlined" style="font-size: 14px;">check_circle</span>
                    <span>System Stable</span>
                </div>
            </div>
        </section>
        """
        st.html(html)

    @staticmethod
    def render_system_status():
        html = """
        <section class="flex flex-col gap-lg w-full h-full">
            <!-- System Health Card -->
            <div class="bg-surface-container border border-outline-variant rounded-xl p-md shadow-sm mb-6">
                <h3 class="font-headline-md text-[18px] text-on-surface mb-md flex items-center gap-sm mb-4">
                    <span class="material-symbols-outlined text-on-surface-variant">monitor_heart</span>
                    System Status
                </h3>
                <div class="flex items-center justify-between bg-surface-container-low border border-outline-variant rounded-lg p-md shadow-sm">
                    <span class="font-body-md text-body-md text-on-surface">API Status</span>
                    <div class="flex items-center gap-sm">
                        <span class="relative flex h-2.5 w-2.5">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary-container opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-primary-container shadow-[0_0_8px_rgba(0,224,255,0.6)]"></span>
                        </span>
                        <span class="font-label-xs text-label-xs text-primary-container uppercase">Operational</span>
                    </div>
                </div>
                <div class="mt-md flex flex-col gap-sm bg-surface-container-low border border-outline-variant rounded-lg p-md shadow-sm mt-4">
                    <div class="flex justify-between items-center mb-2">
                        <span class="font-body-md text-sm text-on-surface-variant">Latency</span>
                        <span class="font-code-sm text-code-sm text-on-surface">42ms</span>
                    </div>
                    <div class="flex justify-between items-center mb-2">
                        <span class="font-body-md text-sm text-on-surface-variant">Model</span>
                        <span class="font-code-sm text-code-sm text-on-surface">v2.4-travel-opt</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="font-body-md text-sm text-on-surface-variant">Tokens/sec</span>
                        <span class="font-code-sm text-code-sm text-on-surface">~850</span>
                    </div>
                </div>
            </div>
            
            <!-- Decorative element -->
            <div class="bg-surface-container border border-outline-variant rounded-xl overflow-hidden h-48 relative flex items-center justify-center group shadow-sm w-full">
                <div class="absolute inset-0 bg-surface-container-low z-0"></div>
                <div class="absolute inset-0 bg-cover bg-center opacity-20 mix-blend-screen z-10" style="background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuAeednc7ObbieY_o6CuEqiOago1uCzXnioCYk7HQjE_xlpcGOEGoPXpNlyKiD7dV9Zj-U8kc8tF0WiUsfoSsMwRFZiD4bsJczbyr-yf74YrACtdaX18pRIDFf4qmPFMPA-9rxkla8JtHZWx94mPXqh2OTADlIC8gH4n4gtjMNsPED3Eb7wHlbopTz2d7cHekpY1hQ9sgioFJ10PEPuIRQxzVb7z5g4tDnYQt4nwMCfqFB3SHcB-bOIAjw')"></div>
                <div class="relative z-20 flex flex-col items-center gap-sm text-on-surface">
                    <span class="material-symbols-outlined text-primary-container opacity-80 mb-2" style="font-size: 32px;">hub</span>
                    <span class="font-code-sm text-xs tracking-widest text-primary-container uppercase">Learning Pipeline Active</span>
                </div>
            </div>
        </section>
        """
        st.html(html)

class PlannerLayout:
    @staticmethod
    def render_configuration_section():
        st.html("<h2 class='font-headline-md text-headline-md text-on-surface mb-lg flex items-center gap-sm mb-6'><span class='material-symbols-outlined text-on-surface-variant'>tune</span> Configure Request</h2>")
        
    @staticmethod
    def render_interests_mockup():
        st.html("""
        <div class="flex flex-col gap-xs w-full mb-4">
            <label class="font-label-xs text-label-xs text-on-surface mb-1">Interests</label>
            <div class="w-full bg-surface-container-low border border-outline-variant rounded-lg p-sm min-h-[100px] ai-pulse shadow-sm">
                <div class="flex flex-wrap gap-sm mb-2">
                    <span class="inline-flex items-center gap-xs px-sm py-1 border border-outline-variant bg-surface-container text-on-surface rounded-full font-label-xs text-label-xs shadow-sm">History <span class="material-symbols-outlined" style="font-size: 14px;">close</span></span>
                    <span class="inline-flex items-center gap-xs px-sm py-1 border border-outline-variant bg-surface-container text-on-surface rounded-full font-label-xs text-label-xs shadow-sm">Food <span class="material-symbols-outlined" style="font-size: 14px;">close</span></span>
                </div>
                <span class="font-code-sm text-code-sm text-primary-container blinking-cursor">|</span>
            </div>
        </div>
        """)

class ResultLayout:
    @staticmethod
    def render_header(city: str, days: int):
        html = f"""
        <div class="space-y-[8px] mb-8">
            <div class="flex items-center gap-[8px] text-primary-fixed-dim mb-2">
                <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">check_circle</span>
                <span class="font-code-sm text-code-sm uppercase tracking-wider text-primary-fixed-dim">Generation Complete</span>
            </div>
            <h1 class="font-display-lg text-display-lg text-on-background mb-2">Your requested itinerary is ready.</h1>
            <p class="font-body-md text-body-md text-on-surface-variant max-w-2xl">The LLM has successfully synthesized your preferences into a structured travel plan. You can review the output, analyze generation metrics, or provide feedback to improve future models.</p>
        </div>
        
        <div class="bg-surface-container-low border border-surface-variant rounded-xl overflow-hidden relative group mb-8">
            <div class="h-48 w-full bg-surface-container-low relative">
                <div class="absolute inset-0 bg-cover bg-center opacity-40 mix-blend-overlay" style="background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuDkIFGG0w5DZHdiVuvXR6T2Cg-vhBbL8wwTM1PSfbMM781FwhDZlZm1Oz-Lx_6PKhWrjqmIcjOsc97iw1J2oXAxiV4CliyJZkF4tFT_u5-UDICCIb84f9k3WOeVPLy43nP5fAPS0G5Xq0LH1T_lN8z6lppWVBWeewta75TL6PzdC6TgRIS06aDxjiIqXCFKIgM2OHj0uVpGicYipDxNxz1He09h1e1MYlIrKgbmeqAZlSlOh1GmYta4_g')"></div>
                <div class="absolute inset-0 bg-background/50"></div>
                <div class="absolute bottom-[16px] left-[16px] right-[16px] flex justify-between items-end">
                    <div>
                        <h2 class="font-display-lg-mobile text-display-lg-mobile text-on-background mb-1">{city.title()}</h2>
                        <p class="font-code-sm text-code-sm text-on-surface-variant">{days} Days • Cultural Immersion • Moderate Pace</p>
                    </div>
                </div>
            </div>
        </div>
        """
        st.html(textwrap.dedent(html))
