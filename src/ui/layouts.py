import streamlit as st
from src.ui import components
from src.ui.icons import Icons

class BaseLayout:
    """Provides standard layout constraints and injections."""
    @staticmethod
    def setup_page(title: str):
        st.set_page_config(page_title=title, page_icon=Icons.ROBOT, layout="wide")
        
        # Inject custom Material Symbols font requirement to ensure icons load properly
        st.markdown("""
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
        """, unsafe_allow_html=True)

class SidebarLayout:
    @staticmethod
    def render(session_id: str, warnings: list = None):
        with st.sidebar:
            components.render_user_profile()
            
            st.button("New Itinerary", use_container_width=True, type="primary", icon=Icons.ADD)
            st.markdown("<hr style='margin: var(--space-4) 0;'/>", unsafe_allow_html=True)
            
            # Workspace Group
            st.markdown("<span class='type-caption'>Workspace</span>", unsafe_allow_html=True)
            st.markdown(f"**{Icons.DASHBOARD} Dashboard**")
            st.markdown(f"{Icons.ROBOT} Itinerary Planner")
            st.markdown(f"{Icons.MAP} Active Trips")
            
            st.markdown("<hr style='margin: var(--space-4) 0;'/>", unsafe_allow_html=True)
            
            # Operations Group
            st.markdown("<span class='type-caption'>Operations</span>", unsafe_allow_html=True)
            st.markdown(f"{Icons.SETTINGS} Configuration")
            st.markdown(f"<span class='type-caption'>Session: {str(session_id)[:8]}...</span>", unsafe_allow_html=True)
            
            if warnings:
                st.markdown("<div style='margin-top: var(--space-4);'>", unsafe_allow_html=True)
                components.render_badge("Degraded", "warning")
                for w in warnings:
                    st.caption(f"⚠️ {w}")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='margin-top: var(--space-4);'>", unsafe_allow_html=True)
                components.render_badge("Operational", "success")
                st.markdown("</div>", unsafe_allow_html=True)

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
                icon="forum",
                trend="+12% this week",
                trend_positive=True
            )
        with col2:
            rating = metrics.get('average_rating', 0)
            rating_str = f"{rating:.1f}" if rating else "N/A"
            components.render_metric(
                label="Avg Rating", 
                value=rating_str,
                icon="star",
                trend="Consistent High Quality",
                trend_positive=True
            )
        with col3:
            fails = metrics.get('generation_failures', 0)
            trend = "Needs Review" if fails > 0 else "System Stable"
            components.render_metric(
                label="Gen Failures", 
                value=str(fails),
                icon="bug_report",
                trend=trend,
                trend_positive=(fails == 0)
            )
            
class PlannerLayout:
    @staticmethod
    def render_configuration_section():
        st.markdown("<h2 class='type-heading' style='margin-top: var(--space-8); margin-bottom: var(--space-4);'><span class='material-symbols-outlined'>tune</span> Configure Request</h2>", unsafe_allow_html=True)

class ResultLayout:
    @staticmethod
    def render_header(city: str, days: int):
        components.render_page_header(
            title=f"{city.title()}",
            subtitle=f"{days} Days • AI Curated Journey",
            icon="map",
            status_badge="Generation Complete"
        )
