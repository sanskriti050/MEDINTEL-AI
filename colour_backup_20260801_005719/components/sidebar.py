import streamlit as st


NAVIGATION = [
    "🏠 Home",
    "📄 Report Analyzer",
    "🩺 Symptom Checker",
    "💊 Medicine Guide",
    "🥗 Diet Planner",
    "📊 Dashboard",
    "ℹ️ About",
]


def render_sidebar():
    """Render the single, polished sidebar navigation for MedIntel AI."""
    with st.sidebar:
        st.markdown(
            """
            <div class="medintel-brand">
                <div class="medintel-logo">🩺</div>
                <div>
                    <div class="medintel-title">MedIntel <span>AI</span></div>
                    <div class="medintel-tagline">Intelligent Healthcare Assistant</div>
                </div>
            </div>
            <p class="medintel-intro">
                Clear, AI-powered health guidance for your reports, symptoms,
                medicines, nutrition and wellness tracking.
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sidebar-rule"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-section-label">HEALTHCARE TOOLS</p>', unsafe_allow_html=True)

        page = st.radio(
            "Navigation",
            NAVIGATION,
            label_visibility="collapsed",
            key="main_navigation",
        )

        st.markdown('<div class="sidebar-rule feature-rule"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-section-label">WHAT YOU CAN DO</p>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="feature-list">
                <div class="sidebar-feature"><span>📄</span><div><b>Report Analyzer</b><small>Upload medical PDFs for AI insights, abnormal values and recommendations.</small></div></div>
                <div class="sidebar-feature"><span>🩺</span><div><b>Symptom Checker</b><small>Understand possible conditions, severity and next steps from your symptoms.</small></div></div>
                <div class="sidebar-feature"><span>💊</span><div><b>Medicine Guide</b><small>Explore uses, dosage, side effects and interactions for medicines.</small></div></div>
                <div class="sidebar-feature"><span>🥗</span><div><b>Diet Planner</b><small>Build a personalized meal plan around your goals and health needs.</small></div></div>
                <div class="sidebar-feature"><span>📊</span><div><b>Health Dashboard</b><small>Track health scores, reports, vital metrics and trends in one place.</small></div></div>
            </div>
            <div class="sidebar-disclaimer">ℹ️ For informational and educational use only — always consult a qualified healthcare professional.</div>
            """,
            unsafe_allow_html=True,
        )

    return page
