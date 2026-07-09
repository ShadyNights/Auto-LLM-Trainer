import streamlit as st


class DashboardState:
    @staticmethod
    def init_state():
        if "conversation_id" not in st.session_state:
            st.session_state.conversation_id = None
        if "active_itinerary_id" not in st.session_state:
            st.session_state.active_itinerary_id = None
        if "last_trip_params" not in st.session_state:
            st.session_state.last_trip_params = None

    @staticmethod
    def set_conversation_id(cid: int):
        st.session_state.conversation_id = cid

    @staticmethod
    def get_conversation_id() -> int | None:
        return st.session_state.get("conversation_id")

    @staticmethod
    def set_active_itinerary_id(iid: int):
        st.session_state.active_itinerary_id = iid

    @staticmethod
    def get_active_itinerary_id() -> int | None:
        return st.session_state.get("active_itinerary_id")

    @staticmethod
    def set_last_trip_params(params: dict):
        st.session_state.last_trip_params = params

    @staticmethod
    def get_last_trip_params() -> dict | None:
        return st.session_state.get("last_trip_params")
