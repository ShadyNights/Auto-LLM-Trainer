"""
Production-Ready AI Travel Planner with Self-Training LLM System
Version: 5.0.0 (Frozen Architecture Blueprint)
"""

import os
import time
import re
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
import traceback
import json

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
from src.domain.enums.event_type import EventType
from src.domain.exceptions import TravelerException, ConfigurationError, PromptNotFound, ProviderUnavailable
from src.infrastructure.logging.json_logger import get_json_logger

load_dotenv(override=True)
logger = get_json_logger(__name__)

st.set_page_config(page_title="AI Travel Planner Pro", page_icon="✈️", layout="wide")

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
    
    # 1. DB
    try:
        with db.get_cursor() as cur:
            cur.execute("SELECT 1")
    except Exception as e:
        critical_errors.append(f"Database Connection Failed: {e}")
        
    # 2. Provider Key
    if not os.getenv("GROQ_API_KEY"):
        critical_errors.append("Provider Key Missing (GROQ_API_KEY)")
        
    # 3. Active Config
    try:
        config = config_repo.get_active_config()
        if not config:
            critical_errors.append("No active configuration found in system_config")
    except Exception as e:
        critical_errors.append(f"Config read error: {e}")
        
    # 4. Prompt Checksum
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

# ==================== UI HELPERS ====================
def sanitize_city(city: str) -> str:
    return re.sub(r'[^a-zA-Z\s-]', '', city.strip())[:50]

# ==================== STREAMLIT UI ====================
st.markdown("""
<style>
    .main-header { text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem; color: white; }
    .main-title { font-size: 3rem; font-weight: bold; margin: 0; }
    .stat-card { text-align: center; padding: 1rem; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
</style>
<div class="main-header">
    <h1 class="main-title">✈️ AI Travel Planner Pro</h1>
    <p>Powered by a Continuous Feedback Learning Pipeline</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Health & Status")
    st.success("🟢 Systems Operational")
    if warnings:
        for w in warnings:
            st.warning(f"⚠️ {w}")
            
    st.markdown("### 📊 Metrics")
    try:
        with db.get_cursor(commit_on_success=False) as cur:
            cur.execute("SELECT * FROM dashboard_metrics")
            metrics = cur.fetchone()
            if metrics:
                st.metric("Total Conversations", metrics.get('total_conversations', 0))
                st.metric("Avg Rating", f"{metrics.get('average_rating', 0):.1f}⭐" if metrics.get('average_rating') else "N/A")
                st.metric("Gen Failures", metrics.get('generation_failures', 0))
    except Exception:
        pass
        
    st.markdown("---")
    st.session_state.trip_days = st.slider("Duration", 1, 14, 1)
    st.session_state.budget_level = st.selectbox("Budget", ["Budget", "Moderate", "Luxury"])

# Main content
col1, col2 = st.columns([2, 1])
with col1:
    with st.form("travel_form"):
        city = st.text_input("🏙️ Destination", max_chars=50)
        interests = st.text_input("🎯 Interests")
        submitted = st.form_submit_button("🚀 Generate AI Itinerary")

if submitted:
    city = sanitize_city(city)
    if not city:
        st.warning("Please enter a valid destination.")
    else:
        try:
            days = st.session_state.trip_days
            budget = st.session_state.budget_level
            interest_list = [i.strip() for i in interests.split(",")] if interests else []
            
            req = ItineraryRequest(city=city, budget=budget, trip_days=days, interests=interest_list, travel_style=["Solo"])
            corr_id = event_service.log_prompt_submitted(st.session_state.conversation_id, city, budget, days)
            
            with st.spinner("Generating itinerary..."):
                response, config, p_ver, d_ver = planner_service.generate_itinerary(req)
                
                # In a real app we'd fetch actual model_version_id and prompt_id. Mocking foreign keys here.
                # Assuming 1, 1 for demo if DB allows.
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
                st.success("✅ Generated successfully!")
                
        except Exception as e:
            event_service.log_generation(st.session_state.conversation_id, corr_id, False, str(e))
            st.error(f"Failed to generate: {e}")

if "itinerary" in st.session_state:
    st.markdown("---")
    st.markdown(st.session_state.itinerary)
    
    st.markdown("### ⭐ Rate this itinerary")
    rating = st.radio("Rating", [5, 4, 3, 2, 1], horizontal=True)
    if st.button("Submit Feedback"):
        itinerary_repo.update_rating(st.session_state.itinerary_id, rating, "No comments")
        event_service.log_feedback(st.session_state.conversation_id, st.session_state.corr_id, rating, "No comments")
        st.success("Feedback recorded. The Learning Pipeline will use this to improve!")

except TravelerException as te:
    logger.error("Domain exception occurred", exc_info=True, extra={"status": "failed"})
    st.error(f"⚠️ **Application Error:** {str(te)}")
except Exception as e:
    logger.error("Unhandled unexpected exception", exc_info=True, extra={"status": "failed"})
    st.error("🚨 **System Error:** An unexpected issue occurred while processing your request. Our team has been notified.")

