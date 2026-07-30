import streamlit as st

NAVIGATION_ITEMS = [
    "🏠  Home",
    "📄  Report Analyzer",
    "🩺  Symptom Checker",
    "💊  Medicine Guide",
    "🥗  Diet Planner",
    "📊  Dashboard",
    "ℹ️  About",
]


def render_sidebar():
    """Render the single, custom MedIntel navigation sidebar."""
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="brand-icon">🏥</div>
                <div>
                    <div class="brand-name">MedIntel <span>AI</span></div>
                    <div class="brand-tagline">YOUR HEALTH, SIMPLIFIED</div>
                </div>
            </div>
            <div class="sidebar-intro">
                <span class="status-dot"></span>
                AI-powered healthcare assistant
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<p class="nav-heading">WORKSPACE</p>', unsafe_allow_html=True)
        page = st.radio(
            "Main navigation",
            NAVIGATION_ITEMS,
            label_visibility="collapsed",
            key="main_navigation",
        )

        st.markdown(
            """
            <div class="sidebar-help-card">
                <div class="help-card-icon">✦</div>
                <div>
                    <div class="help-card-title">Need a quick start?</div>
                    <div class="help-card-copy">Upload a medical report to get clear AI insights.</div>
                </div>
            </div>
            <div class="sidebar-footer">
                <span>MedIntel AI</span><span>•</span><span>For informational use only</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return page
