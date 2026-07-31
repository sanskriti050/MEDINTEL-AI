import streamlit as st


def render_sidebar():
    """Render the application sidebar with navigation and health tips."""

    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:10px 0 20px 0;">
            <h2 style="color:white;margin:0;">🏥 MedIntel AI</h2>
            <p style="color:#64748B;font-size:0.8rem;margin:4px 0 0 0;">AI Healthcare Assistant</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        page = st.radio(
            "Navigation",
            [
                "🏠 Home",
                "📄 Report Analyzer",
                "🩺 Symptom Checker",
                "💊 Medicine Guide",
                "🥗 Diet Planner",
                "📊 Dashboard",
                "ℹ About"
            ],
            label_visibility="collapsed"
        )

        st.divider()

        st.markdown("**💡 Quick Tip**")
        st.info("Upload a PDF medical report on the **Report Analyzer** page for instant AI analysis.")

        st.markdown("""
        <div style="
            position:fixed;
            bottom:20px;
            font-size:0.75rem;
            color:#475569;
            text-align:center;
        ">
            MedIntel AI v1.0 | For informational use only
        </div>
        """, unsafe_allow_html=True)

    return page
