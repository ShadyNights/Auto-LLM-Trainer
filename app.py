"""
Production-Ready AI Travel Planner with Self-Training LLM System
Version: 5.1.0 (UI/UX Redesign)
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

# UI Components
from src.ui.styles import inject_styles
from src.ui.layout import render_header, render_section
from src.ui.components import (
    render_metric, render_empty_state, 
    render_badge, render_loading, render_card
)

load_dotenv(override=True)
logger = get_json_logger(__name__)

st.set_page_config(page_title="Traveler LLM", page_icon="✈️", layout="wide")
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
    with st.sidebar:
        # 1. Workspace
        render_section("Workspace", icon="🛠️")
        st.markdown(f"<p class='text-muted'>Session ID: <code>{st.session_state.conversation_id}</code></p>", unsafe_allow_html=True)
        st.markdown("<hr/>", unsafe_allow_html=True)
        
        # 2. Health
        render_section("System Health", icon="⚙️")
        if warnings:
            st.markdown(render_badge("Degraded", "error"), unsafe_allow_html=True)
            for w in warnings:
                st.caption(f"⚠️ {w}")
        else:
            st.markdown(render_badge("Operational", "primary"), unsafe_allow_html=True)
        st.markdown("<hr/>", unsafe_allow_html=True)
            
        # 3. Configuration
        render_section("Configuration", icon="🧠")
        try:
            config = config_repo.get_active_config()
            st.markdown(f"<p class='text-muted' style='margin:0;'>Provider: <b>Groq</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p class='text-muted' style='margin:0;'>Prompt: <b>v1</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p class='text-muted' style='margin:0;'>Dataset: <b>ds-v1</b></p>", unsafe_allow_html=True)
        except:
            st.markdown(render_badge("Config Error", "error"), unsafe_allow_html=True)
        st.markdown("<hr/>", unsafe_allow_html=True)

        # 4. Metrics
        render_section("Metrics", icon="📊")
        try:
            with db.get_cursor(commit_on_success=False) as cur:
                cur.execute("SELECT * FROM dashboard_metrics")
                metrics = cur.fetchone()
                if metrics:
                    render_metric("Total Conversations", str(metrics.get('total_conversations', 0)))
                    st.markdown("<br/>", unsafe_allow_html=True)
                    
                    rating = metrics.get('average_rating', 0)
                    rating_str = f"{rating:.1f}" if rating else "N/A"
                    render_metric("Avg Rating", rating_str, "Stable", "neutral")
                    st.markdown("<br/>", unsafe_allow_html=True)
                    
                    fails = metrics.get('generation_failures', 0)
                    fail_trend = "Needs Review" if fails > 0 else "Optimal"
                    fail_color = "error" if fails > 0 else "primary"
                    render_metric("Gen Failures", str(fails), fail_trend, fail_color)
        except Exception:
            render_metric("Metrics", "Offline", "DB Error", "error")

    # ==================== MAIN CONTENT ====================
    render_header(
        title="Traveler LLM", 
        subtitle="Automated itinerary curation powered by a Continuous Feedback Learning Pipeline.",
        icon="✈️"
    )

    # 1. Configuration (Input Form)
    with st.container():
        render_section("Configure Request", "Set the parameters for your next adventure.")
        with st.form("travel_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                city = st.text_input("Destination City", max_chars=50, placeholder="e.g. Kyoto, Japan")
                days = st.number_input("Travel Duration (Days)", min_value=1, max_value=14, value=5)
            with col_b:
                interests = st.text_input("Core Interests", placeholder="e.g. History, Food, Hiking")
                budget = st.selectbox("Budget Profile", ["Budget", "Moderate", "Luxury"])
                
            st.markdown("<hr style='margin-top:8px;'/>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Generate Premium Itinerary")

    # 2. Generation Phase
    if submitted:
        city_clean = sanitize_city(city)
        if not city_clean:
            st.warning("Please enter a valid destination.")
        else:
            interest_list = [i.strip() for i in interests.split(",")] if interests else []
            req = ItineraryRequest(city=city_clean, budget=budget, trip_days=days, interests=interest_list, travel_style=["Solo"])
            corr_id = event_service.log_prompt_submitted(st.session_state.conversation_id, city_clean, budget, days)
            
            st.markdown("<br/>", unsafe_allow_html=True)
            render_section("Generation in Progress", "The LLM is processing your request...")
            render_loading()
            
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
                st.rerun() # Refresh to show results cleanly
                
            except Exception as e:
                event_service.log_generation(st.session_state.conversation_id, corr_id, False, str(e))
                st.error(f"Failed to generate: {e}")

    # 3. Result, Analytics & Feedback Flow
    if "itinerary" in st.session_state and not submitted:
        st.markdown("<br/>", unsafe_allow_html=True)
        render_section("Generated Results", "Your requested itinerary is ready.")
        
        tab1, tab2, tab3 = st.tabs(["📝 Itinerary", "⚙️ Analytics", "⭐ Feedback"])
        
        with tab1:
            result_html = f"{st.session_state.itinerary}"
            render_card(result_html, active_glow=True)
            
        with tab2:
            analytics_html = f"""
            <div class="l-stack">
                <div>
                    <p style="margin:0;">Itinerary ID</p>
                    <p style="font-family:monospace; margin:0; color:var(--c-primary);">{st.session_state.itinerary_id}</p>
                </div>
                <div>
                    <p style="margin:0;">Correlation ID</p>
                    <p style="font-family:monospace; margin:0; color:var(--c-primary);">{st.session_state.corr_id}</p>
                </div>
                <div>
                    <p style="margin:0;">Status</p>
                    {render_badge('Pipeline Queued', 'primary')}
                </div>
            </div>
            """
            render_card(analytics_html)
            
        with tab3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("#### Rate this Itinerary")
            st.markdown("<p class='text-secondary'>Your feedback trains the model via the Continuous Feedback Learning Pipeline.</p>", unsafe_allow_html=True)
            
            with st.form("feedback_form"):
                rating = st.radio("Quality Rating", [5, 4, 3, 2, 1], horizontal=True)
                comments = st.text_area("Optional Comments")
                submit_fb = st.form_submit_button("Submit Feedback")
                
                if submit_fb:
                    itinerary_repo.update_rating(st.session_state.itinerary_id, rating, comments)
                    event_service.log_feedback(st.session_state.conversation_id, st.session_state.corr_id, rating, comments)
                    st.success("✅ Feedback securely recorded and queued for pipeline processing.")
            st.markdown("</div>", unsafe_allow_html=True)

except TravelerException as te:
    logger.error("Domain exception occurred", exc_info=True, extra={"status": "failed"})
    st.error(f"⚠️ **Application Error:** {str(te)}")
except Exception as e:
    logger.error("Unhandled unexpected exception", exc_info=True, extra={"status": "failed"})
    st.error("🚨 **System Error:** An unexpected issue occurred while processing your request. Our team has been notified.")
