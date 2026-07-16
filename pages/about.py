import streamlit as st


def show_about():
    st.title("ℹ️ About MedIntel AI")
    st.caption("AI-Powered Intelligent Healthcare Assistant")

    st.divider()

    st.write("""
**MedIntel AI** is an intelligent healthcare platform that uses advanced AI to help users understand their medical reports, symptoms, medications, and diet — all in one place.
""")

    st.divider()

    st.subheader("🚀 Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📄 **Medical Report Analyzer**\n\nUpload PDF reports and get AI-powered insights including health score, abnormal values, and recommendations.")
        st.info("🩺 **Symptom Checker**\n\nDescribe your symptoms and receive possible conditions, severity assessment, and home remedies.")

    with col2:
        st.info("💊 **Medicine Guide**\n\nSearch any medicine for detailed information on uses, dosage, side effects, and interactions.")
        st.info("🥗 **Diet Planner**\n\nGet a personalized meal plan based on your age, weight, health goals, and medical conditions.")

    with col3:
        st.info("📊 **Health Dashboard**\n\nTrack your health metrics, view trends, and monitor risk levels over time.")
        st.info("🤖 **Powered by Groq AI**\n\nUses LLaMA 3.3 70B model via Groq for fast and accurate medical analysis.")

    st.divider()

    st.subheader("⚠️ Disclaimer")
    st.warning("""
MedIntel AI is designed for **informational and educational purposes only**.

- It is **NOT** a substitute for professional medical advice, diagnosis, or treatment.
- Always consult a qualified healthcare provider for medical decisions.
- In case of emergency, contact your local emergency services immediately.
""")

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("🛠️ Tech Stack")
        st.markdown("""
- **Frontend:** Streamlit
- **AI Model:** LLaMA 3.3 70B via Groq
- **PDF Parsing:** pdfplumber
- **Charts:** Plotly
- **Language:** Python 3.10+
""")

    with col_b:
        st.subheader("📦 Version Info")
        st.markdown("""
- **App Version:** 1.0.0
- **Release:** July 2026
- **Status:** Active Development
""")
