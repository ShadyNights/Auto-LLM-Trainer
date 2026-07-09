import streamlit as st
from src.ui import components
from src.ui.icons import Icons

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
            st.html("<div style='margin-bottom: var(--space-6);'><span class='type-display' style='font-size: 24px; color: var(--color-accent-primary); letter-spacing: -0.02em;'>Traveler LLM</span></div>")
            
            components.render_user_profile()
            
            st.button("New Itinerary", use_container_width=True, type="primary", icon=Icons.ADD)
            
            st.html("<div style='margin: var(--space-6) 0;'></div>")
            
            # Workspace Group
            st.html("<span class='type-caption' style='padding-left: var(--space-4); margin-bottom: var(--space-2); display: block;'>Workspace</span>")
            components.render_sidebar_link("Dashboard", Icons.DASHBOARD, is_active=False)
            components.render_sidebar_link("Itinerary Planner", Icons.SPARKLES, is_active=True)
            components.render_sidebar_link("Active Trips", Icons.MAP, is_active=False)
            
            st.html("<div style='margin: var(--space-6) 0;'></div>")
            
            # Operations Group
            st.html("<span class='type-caption' style='padding-left: var(--space-4); margin-bottom: var(--space-2); display: block;'>Operations</span>")
            components.render_sidebar_link("System Health", Icons.HEARTBEAT, is_active=False)
            components.render_sidebar_link("Configuration", Icons.SETTINGS, is_active=False)
            
            st.html("<div style='margin-top: auto; border-top: 1px solid var(--color-border-default); padding-top: var(--space-4);'></div>")
            
            components.render_sidebar_link("Help", Icons.HELP, is_active=False)
            components.render_sidebar_link("Feedback", Icons.FEEDBACK, is_active=False)

            if warnings:
                st.html("<div style='margin-top: var(--space-4);'>")
                components.render_badge("Degraded", "warning")
                for w in warnings:
                    st.caption(f"⚠️ {w}")
                st.html("</div>")

class DashboardLayout:
    @staticmethod
    def render_hero():
        components.render_page_header(
            title="Traveler LLM",
            subtitle="Automated itinerary curation powered by a Continuous Feedback Learning Pipeline.",
            status_badge="Pipeline Active"
        )
        
    @staticmethod
    def render_metrics(metrics: dict):
        col1, col2, col3 = st.columns(3)
        with col1:
            components.render_metric(
                label="Total Conversations", 
                value=str(metrics.get('total_conversations', 0)),
                icon=Icons.FORUM,
                trend="+12% this week",
                trend_positive=True
            )
        with col2:
            rating = metrics.get('average_rating', 0)
            rating_str = f"{rating:.1f}" if rating else "N/A"
            components.render_metric(
                label="Avg Rating", 
                value=rating_str,
                icon=Icons.STAR,
                trend="Consistent High Quality",
                trend_positive=True
            )
        with col3:
            fails = metrics.get('generation_failures', 0)
            trend = "Needs Review" if fails > 0 else "System Stable"
            components.render_metric(
                label="Gen Failures", 
                value=str(fails),
                icon=Icons.BUG,
                trend=trend,
                trend_positive=(fails == 0)
            )
            
class PlannerLayout:
    @staticmethod
    def render_configuration_section():
        st.html("<h2 class='type-heading' style='margin-top: var(--space-8); margin-bottom: var(--space-4); display: flex; align-items: center; gap: var(--space-2);'><span class='material-symbols-outlined' style='color: var(--color-text-muted);'>tune</span> Configure Request</h2>")

class ResultLayout:
    @staticmethod
    def render_header(city: str, days: int):
        components.render_page_header(
            title=f"{city.title()}",
            subtitle=f"{days} Days • AI Curated Journey",
            icon=Icons.MAP,
            status_badge="Generation Complete"
        )
