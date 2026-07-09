import streamlit as st

from .components import render_badge, render_card


def render_itinerary_card(itinerary_text: str):
    """Renders the AI generated itinerary result."""
    render_card(itinerary_text, active_glow=True)


def render_analytics_card(itinerary_id: str, corr_id: str):
    """Renders telemetry and pipeline tracking data for an itinerary."""
    analytics_html = f'<div class="l-stack"><div><p class="c-meta-label">Itinerary ID</p><p class="c-meta-value">{itinerary_id}</p></div><div><p class="c-meta-label">Correlation ID</p><p class="c-meta-value">{corr_id}</p></div><div><p class="c-meta-label">Status</p>{render_badge("Pipeline Queued", "primary")}</div></div>'
    render_card(analytics_html)


def render_feedback_form() -> tuple[int | None, str | None, bool]:
    """
    Renders the continuous feedback learning loop form.
    Returns: (rating, comments, is_submitted)
    """
    st.markdown("<div class='c-card'>", unsafe_allow_html=True)
    st.markdown("#### Rate this Itinerary")
    st.markdown(
        "<p class='c-meta-label'>Your feedback trains the model via the Continuous Feedback Learning Pipeline.</p>",
        unsafe_allow_html=True,
    )

    with st.form("feedback_form"):
        rating = st.radio("Quality Rating", [5, 4, 3, 2, 1], horizontal=True)
        comments = st.text_area("Optional Comments")
        submit_fb = st.form_submit_button("Submit Feedback")

    st.markdown("</div>", unsafe_allow_html=True)
    return rating, comments, submit_fb
