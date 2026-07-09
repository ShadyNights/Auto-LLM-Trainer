"""
Production-Ready AI Travel Planner with Self-Training LLM System
Version: 5.1.0 (Modular UI Re-architecture)
"""

import os
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

# Dedicated UI Layer Imports
from src.ui.styles import inject_styles
from src.ui.navigation import render_sidebar
from src.ui.forms import render_travel_form
from src.ui.dashboard import render_hero_dashboard, render_processing_state, render_results_dashboard
from src.ui.helpers import sanitize_text

from src.repositories.analytics_repository import AnalyticsRepository
from src.repositories.metrics_repository import MetricsRepository
from src.repositories.trip_repository import TripRepository
from src.repositories.database_repository import DatabaseRepository
from src.ui.state.dashboard_state import DashboardState
from src.ui.views.trip_summary import render_trip_summary_view
from src.ui.views.ai_metrics import render_ai_metrics_view
from src.ui.views.analytics import render_analytics_view
from src.ui.views.database_manager import render_database_manager_view

load_dotenv(override=True)
logger = get_json_logger(__name__)

st.set_page_config(page_title="Traveler LLM", page_icon="✈️", layout="wide")
inject_styles()
DashboardState.init_state()

try:
    # ==================== BOOTSTRAP DEPENDENCIES ====================
    db = DatabaseConnection()
    config_repo = ConfigRepository(db)
    prompt_repo = PromptRepository()
    event_repo = EventRepository(db)
    training_repo = TrainingRepository(db)
    itinerary_repo = ItineraryRepository(db)
    analytics_repo = AnalyticsRepository(db)
    metrics_repo = MetricsRepository(db)
    trip_repo = TripRepository(db)
    database_repo = DatabaseRepository(db)

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
            
        config_active = False
        try:
            config = config_repo.get_active_config()
            if config: config_active = True
            else: critical_errors.append("No active configuration found in system_config")
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
            
        return critical_errors, warnings, config_active

    critical, warnings, config_active = run_health_checks()
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

    # Fetch Metrics for Sidebar
    metrics_data = None
    try:
        with db.get_cursor(commit_on_success=False) as cur:
            cur.execute("SELECT * FROM dashboard_metrics")
            metrics_data = cur.fetchone()
    except Exception:
        pass

    # ==================== SIDEBAR ====================
    current_page = render_sidebar(st.session_state.conversation_id, warnings, config_active)

    # ==================== MAIN CONTENT (ROUTING) ====================
    if current_page == "Generator":
        render_hero_dashboard(metrics_data)

        # 1. Configuration (Input Form)
        with st.container():
            city, days, interests, budget, travel_style, submitted = render_travel_form()

        # 2. Generation Phase
        if submitted:
            city_clean = sanitize_text(city)
            if not city_clean:
                st.warning("Please enter a valid destination.")
            else:
                interest_list = [i.strip() for i in interests.split(",")] if interests else []
                # Store params for the Trip Summary page
                DashboardState.set_last_trip_params({'city': city_clean, 'days': days, 'budget': budget, 'interests': interest_list, 'travel_style': travel_style})
                
                req = ItineraryRequest(city=city_clean, budget=budget, trip_days=days, interests=interest_list, travel_style=[travel_style])
                corr_id = event_service.log_prompt_submitted(st.session_state.conversation_id, city_clean, budget, days)
                
                render_processing_state()
                
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
                    DashboardState.set_active_itinerary_id(itin_id)
                    st.rerun() # Refresh to show results cleanly
                    
                except Exception as e:
                    event_service.log_generation(st.session_state.conversation_id, corr_id, False, str(e))
                    st.error(f"Failed to generate: {e}")

        # 3. Result, Analytics & Feedback Flow
        if "itinerary" in st.session_state and not submitted:
            rating, comments, submit_fb = render_results_dashboard(
                st.session_state.itinerary,
                st.session_state.itinerary_id,
                st.session_state.corr_id
            )
            
            if submit_fb:
                itinerary_repo.update_rating(st.session_state.itinerary_id, rating, comments)
                event_service.log_feedback(st.session_state.conversation_id, st.session_state.corr_id, rating, comments)
                st.success("✅ Feedback securely recorded and queued for pipeline processing.")
                
    elif current_page == "Trip Summary":
        render_trip_summary_view(trip_repo)
    elif current_page == "AI Metrics":
        render_ai_metrics_view(metrics_repo)
    elif current_page == "Analytics Dashboard":
        render_analytics_view(analytics_repo)
    elif current_page == "Database Manager":
        render_database_manager_view(database_repo)

except TravelerException as te:
    logger.error("Domain exception occurred", exc_info=True, extra={"status": "failed"})
    st.error(f"⚠️ **Application Error:** {str(te)}")
except Exception as e:
    logger.error("Unhandled unexpected exception", exc_info=True, extra={"status": "failed"})
    st.error("🚨 **System Error:** An unexpected issue occurred while processing your request. Our team has been notified.")
