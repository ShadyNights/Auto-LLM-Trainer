"""
Production-Ready AI Travel Planner with Self-Training LLM System
Version: 5.2.0 (Design System Architecture Migration)
"""

import os
import re
import streamlit as st
from dotenv import load_dotenv

from src.infrastructure.database.connection import DatabaseConnection
from src.repositories.config_repository import ConfigRepository
from src.repositories.prompt_repository import PromptRepository
from src.repositories.event_repository import EventRepository
from src.repositories.training_repository import TrainingRepository
from src.repositories.itinerary_repository import ItineraryRepository
from src.providers.groq_provider import GroqProvider

from src.services.planner.planner_service import PlannerService
from src.services.event.event_service import EventService
from src.domain.dto.itinerary_request import ItineraryRequest
from src.domain.exceptions import TravelerException
from src.infrastructure.logging.json_logger import get_json_logger

# UI Design System
from src.ui.styles import inject_styles
from src.ui.layouts import BaseLayout, SidebarLayout, DashboardLayout, PlannerLayout, ResultLayout
from src.ui.components import render_badge, render_card, render_ai_card, render_empty_state
from src.ui.icons import Icons

load_dotenv(override=True)
logger = get_json_logger(__name__)

# Initialize layout constraints and dependencies
BaseLayout.setup_page("Traveler LLM Dashboard")
inject_styles()

try:
    # ==================== BOOTSTRAP DEPENDENCIES ====================
    db = DatabaseConnection()
    config_repo = ConfigRepository(db)
    prompt_repo = PromptRepository()
    event_repo = EventRepository(db)
    training_repo = TrainingRepository(db)
    itinerary_repo = ItineraryRepository(db)

    provider = GroqProvider()
    planner_service = PlannerService(config_repo, prompt_repo, provider)
    event_service = EventService(event_repo)

    # ==================== HEALTH CHECKS ====================
    def run_health_checks():
        critical_errors = []
        warnings = []
        try:
            with db.get_cursor() as cur:
                cur.execute("SELECT 1")
        except Exception as e:
            critical_errors.append(f"Database Connection Failed: {e}")
            
        if not os.getenv("GROQ_API_KEY"):
            critical_errors.append("Provider Key Missing (GROQ_API_KEY)")
            
        try:
            config = config_repo.get_active_config()
            if not config:
                critical_errors.append("No active configuration found in system_config")
        except Exception as e:
            critical_errors.append(f"Config read error: {e}")
            
        try:
            prompt_text = prompt_repo.get_prompt_text("v1")
            if not prompt_text:
                warnings.append("Active prompt (v1) could not be loaded from filesystem.")
            elif len(prompt_text.strip()) == 0:
                warnings.append("Active prompt (v1) is empty.")
        except Exception as e:
            warnings.append(f"Prompt load warning: {e}")
            
        return critical_errors, warnings

    critical, warnings = run_health_checks()
    if critical:
        st.error("🚨 **CRITICAL SYSTEM FAILURE**")
        for err in critical:
            st.error(err)
        st.stop()
        
    # ==================== SESSION STATE ====================
    if 'conversation_id' not in st.session_state:
        try:
            st.session_state.conversation_id = event_service.start_conversation()
        except Exception as e:
            st.error("Failed to start session. DB might be uninitialized. Run setup_database.py.")
            st.stop()

    def sanitize_city(city: str) -> str:
        return re.sub(r'[^a-zA-Z\s-]', '', city.strip())[:50]

    # ==================== SIDEBAR ====================
    SidebarLayout.render(st.session_state.conversation_id, warnings)

    # ==================== MAIN CONTENT (DASHBOARD LAYER) ====================
    # The new DashboardLayout contains the exact Tailwind grids for Hero and Metrics
    st.html("<div class='max-w-[1280px] mx-auto px-[16px] md:px-[24px] py-[32px] space-y-[32px]'>")
    
    col_main, col_sidebar = st.columns([2, 1], gap="large")
    
    with col_main:
        DashboardLayout.render_hero()
        
        try:
            with db.get_cursor(commit_on_success=False) as cur:
                cur.execute("SELECT * FROM dashboard_metrics")
                metrics = cur.fetchone()
                if metrics:
                    DashboardLayout.render_metrics(metrics)
        except Exception:
            pass # Metrics fallback silent for UI

        # ==================== PLANNER LAYER ====================
        st.html("<div class='bg-surface-container border border-outline-variant rounded-xl p-xl shadow-sm'>")
        PlannerLayout.render_configuration_section()
        
        with st.form("travel_form", clear_on_submit=False, border=False):
            st.html("<h3 class='font-label-xs text-label-xs text-on-surface-variant uppercase tracking-wider border-b border-outline-variant pb-xs mb-4'>Trip Basics</h3>")
            
            col_a, col_b = st.columns(2)
            with col_a:
                city = st.text_input("Destination City", max_chars=50, placeholder="e.g. Kyoto, Japan", value="Kyoto, Japan")
            with col_b:
                days = st.number_input("Travel Duration (Days)", min_value=1, max_value=14, value=5)
                
            st.html("<div style='margin-bottom: var(--space-6);'></div>")
            st.html("<h3 class='font-label-xs text-label-xs text-on-surface-variant uppercase tracking-wider border-b border-outline-variant pb-xs mb-4'>Preferences</h3>")
            
            PlannerLayout.render_interests_mockup()
            interests = st.text_input("Core Interests (Fallback)", placeholder="Type interests here", label_visibility="collapsed")
            budget = st.radio("Budget Profile", ["Budget", "Moderate", "Luxury"], horizontal=True, index=1)
                
            st.html("<div class='mt-md pt-md border-t border-outline-variant'></div>")
            submitted = st.form_submit_button("Generate Premium Itinerary", type="primary", use_container_width=True)
        st.html("</div>")

    with col_sidebar:
        DashboardLayout.render_system_status()
        
    st.html("</div>")

    # ==================== GENERATION LAYER ====================
    if submitted:
        city_clean = sanitize_city(city)
        if not city_clean:
            st.warning("Please enter a valid destination.")
        else:
            interest_list = [i.strip() for i in interests.split(",")] if interests else []
            req = ItineraryRequest(city=city_clean, budget=budget, trip_days=days, interests=interest_list, travel_style=["Solo"])
            corr_id = event_service.log_prompt_submitted(st.session_state.conversation_id, city_clean, budget, days)
            
            st.markdown("<br/>", unsafe_allow_html=True)
            render_ai_card("Synthesizing Request", "Connecting to Language Model Pipeline...", "thinking")
            
            try:
                response, config, p_ver, d_ver = planner_service.generate_itinerary(req)
                
                itin_id = itinerary_repo.create_itinerary(
                    conversation_id=st.session_state.conversation_id,
                    itinerary_text=response.text,
                    prompt_id=config.active_prompt_id,
                    model_version_id=config.active_model_id,
                    config_snapshot={"temperature": 0.7, "max_tokens": 2000, "provider": "Groq"},
                    word_count=len(response.text.split())
                )
                
                training_repo.enqueue(itin_id)
                event_service.log_generation(st.session_state.conversation_id, corr_id, True)
                
                st.session_state.itinerary = response.text
                st.session_state.itinerary_id = itin_id
                st.session_state.corr_id = corr_id
                st.rerun() 
                
            except Exception as e:
                event_service.log_generation(st.session_state.conversation_id, corr_id, False, str(e))
                render_ai_card("Generation Failed", str(e), "error")

    # ==================== RESULTS LAYER ====================
    if "itinerary" in st.session_state and not submitted:
        st.html("<div class='max-w-[1280px] mx-auto px-[16px] md:px-[24px] py-[32px] space-y-[32px] animate-fade-in pt-[8px]'>")
        
        ResultLayout.render_header("Kyoto, Japan", 5) # Placeholder values until state holds request data
        
        st.html("""
        <div class="border-b border-outline-variant mb-6">
            <nav aria-label="Tabs" class="flex gap-[8px] px-[8px]">
                <button class="font-body-md text-body-md font-medium text-primary-fixed-dim bg-surface-container-high rounded-t-lg px-[16px] py-[8px] transition-colors">Itinerary</button>
                <button class="font-body-md text-body-md font-medium text-on-surface-variant hover:text-on-background hover:bg-surface-container rounded-t-lg px-[16px] py-[8px] transition-colors">Analytics</button>
                <button class="font-body-md text-body-md font-medium text-on-surface-variant hover:text-on-background hover:bg-surface-container rounded-t-lg px-[16px] py-[8px] transition-colors">Feedback</button>
            </nav>
        </div>
        """)
        
        tab1, tab2, tab3 = st.tabs(["📝 Itinerary", "⚙️ Analytics", "⭐ Feedback"])
        
        with tab1:
            st.html("""
            <div class="p-[24px] space-y-[40px] bg-background">
                <!-- Day 1 -->
                <div class="relative pl-[32px] border-l border-outline-variant">
                    <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-primary-container ring-4 ring-background border border-primary-fixed"></div>
                    <h3 class="font-headline-md text-headline-md text-primary-fixed-dim mb-[8px]">AI Generated Itinerary</h3>
                    <p class="font-body-md text-body-md text-on-surface-variant mb-[24px]">Synthesized based on your preferences.</p>
                    
                    <div class="space-y-[16px]">
                        <div class="bg-surface-container rounded-lg p-[16px] flex gap-[16px] border border-surface-variant shadow-sm">
                            <div class="mt-1 text-on-surface-variant">
                                <span class="material-symbols-outlined">auto_awesome</span>
                            </div>
                            <div class="w-full">
            """)
            st.markdown(st.session_state.itinerary)
            st.html("""
                            </div>
                        </div>
                        
                        <!-- AI Suggestion Item -->
                        <div class="bg-surface-container-low border border-primary-fixed-dim/30 rounded-lg p-[16px] relative overflow-hidden shadow-sm mt-4">
                            <div class="flex gap-[16px] relative z-10">
                                <div class="mt-1 text-primary-fixed-dim">
                                    <span class="material-symbols-outlined">psychology</span>
                                </div>
                                <div>
                                    <div class="font-body-md text-body-md font-semibold text-on-background flex items-center gap-[8px]">
                                        Dynamic Tailoring
                                        <span class="bg-primary-container text-on-primary-container font-label-xs text-label-xs px-2 py-0.5 rounded-full uppercase tracking-wider">AI Note</span>
                                    </div>
                                    <p class="font-body-md text-body-md text-on-surface-variant mt-2 blinking-cursor">This itinerary was dynamically tailored based on your historical preferences and active learning pipeline state.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """)
            
        with tab2:
            render_card("Pipeline Analytics", f"Itinerary ID: {st.session_state.itinerary_id}\nCorrelation ID: {st.session_state.corr_id}")
            
        with tab3:
            with st.container():
                st.markdown("<div class='bg-surface-container border border-outline-variant rounded-xl p-xl shadow-sm'>", unsafe_allow_html=True)
                st.markdown("<h3 class='font-headline-md text-headline-md text-on-surface mb-lg flex items-center gap-sm'>Rate this Generation</h3>", unsafe_allow_html=True)
                with st.form("feedback_form"):
                    rating = st.radio("Quality Rating", [5, 4, 3, 2, 1], horizontal=True)
                    comments = st.text_area("Optional Comments")
                    submit_fb = st.form_submit_button("Submit Feedback", type="primary")
                    
                    if submit_fb:
                        itinerary_repo.update_rating(st.session_state.itinerary_id, rating, comments)
                        event_service.log_feedback(st.session_state.conversation_id, st.session_state.corr_id, rating, comments)
                        st.success("✅ Feedback securely recorded and queued for pipeline processing.")
                st.markdown("</div>", unsafe_allow_html=True)
                
        st.html("</div>")

except TravelerException as te:
    logger.error("Domain exception occurred", exc_info=True, extra={"status": "failed"})
    st.error(f"⚠️ **Application Error:** {str(te)}")
except Exception as e:
    logger.error("Unhandled unexpected exception", exc_info=True, extra={"status": "failed"})
    st.error("🚨 **System Error:** An unexpected issue occurred while processing your request. Our team has been notified.")
