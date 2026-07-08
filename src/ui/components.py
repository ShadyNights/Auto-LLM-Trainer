import streamlit as st
from typing import Optional, Any

def render_hero(title: str, subtitle: str, icon: str = "✈️"):
    st.markdown(f"""
    <div class="ui-hero">
        <h1>{icon} {title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_card(content_html: str):
    st.markdown(f"""
    <div class="ui-card">
        {content_html}
    </div>
    """, unsafe_allow_html=True)

def render_metric(title: str, value: str, icon: str, trend: str = None, trend_color: str = "neutral"):
    trend_html = ""
    if trend:
        trend_html = f"""
        <div class="ui-metric-footer">
            <span class="ui-badge {trend_color}">{trend}</span>
        </div>
        """
        
    st.markdown(f"""
    <div class="ui-card ui-metric">
        <div class="ui-metric-header">
            <span>{icon}</span>
            <span>{title}</span>
        </div>
        <div class="ui-metric-value">{value}</div>
        {trend_html}
    </div>
    """, unsafe_allow_html=True)

def render_badge(text: str, status: str = "neutral") -> str:
    return f'<span class="ui-badge {status}">{text}</span>'

def render_empty_state(icon: str, title: str, description: str):
    st.markdown(f"""
    <div class="ui-empty-state">
        <div style="font-size: 3rem;">{icon}</div>
        <h3>{title}</h3>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_skeleton_loader():
    st.markdown("""
    <div class="ui-card">
        <div class="ui-skeleton title"></div>
        <div class="ui-skeleton text"></div>
        <div class="ui-skeleton text"></div>
        <div class="ui-skeleton text short"></div>
        <br/>
        <div class="ui-skeleton text"></div>
        <div class="ui-skeleton text short"></div>
    </div>
    """, unsafe_allow_html=True)
