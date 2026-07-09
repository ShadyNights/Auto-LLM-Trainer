import streamlit as st

from .layout import render_section


def render_travel_form() -> tuple[str, int, str, str, str, bool]:
    """
    Renders the main travel configuration form inside an elevated card.
    Returns: (city, days, interests, budget, travel_style, is_submitted)
    """
    st.markdown("<div class='c-card'>", unsafe_allow_html=True)
    render_section("Trip Configuration", "Set the parameters for your next adventure.", icon="tune")

    with st.form("travel_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            city = st.text_input("Destination City", max_chars=50, placeholder="e.g. Kyoto, Japan")
            st.caption("City you are traveling to.")
            days = st.number_input("Travel Duration (Days)", min_value=1, max_value=14, value=5)
            st.caption("Between 1 and 14 days.")
        with col_b:
            interests = st.text_input("Core Interests", placeholder="e.g. History, Food, Hiking")
            st.caption("Comma-separated topics.")
            budget = st.selectbox("Budget Profile", ["Budget", "Moderate", "Luxury"])
            st.caption("Select your spending style.")
            travel_style = st.selectbox("Travel Style", ["Solo", "Duo", "Family", "Friends", "Business"])
            st.caption("Who are you traveling with?")

        st.markdown("<hr style='margin-top:8px; border-color:var(--c-outline-variant);'/>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Generate Premium Itinerary")

    st.markdown("</div>", unsafe_allow_html=True)
    return city, days, interests, budget, travel_style, submitted


def render_search_input(placeholder: str = "Search...") -> str:
    """Renders a modern search input (mock component for full library compliance)."""
    return st.text_input("Search", placeholder=placeholder, label_visibility="collapsed")


def render_segmented_control(label: str, options: list[str], default: str) -> str:
    """Renders a segmented control (mapped to st.radio horizontal for Streamlit)."""
    return st.radio(label, options, index=options.index(default) if default in options else 0, horizontal=True)
