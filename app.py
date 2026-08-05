import streamlit as st

from pages.home import show_home
from pages.report import show_report
from pages.symptom import show_symptom
from pages.medicine import show_medicine
from pages.diet import show_diet
from pages.dashboard import show_dashboard
from pages.about import show_about
from styles import load_css
from components.sidebar import render_sidebar   # ← uses components/sidebar.py

st.set_page_config(
    page_title="MedIntel AI",
    page_icon="🏥",
    layout="wide"
)
load_css()

# ── Render sidebar and capture selected page ─────────────────────────────────
page = render_sidebar()

# ── Route to the correct page ────────────────────────────────────────────────
if page == "🏠 Home":
    show_home()

elif page == "📄 Report Analyzer":
    show_report()

elif page == "🩺 Symptom Checker":
    show_symptom()

elif page == "💊 Medicine Guide":
    show_medicine()

elif page == "🥗 Diet Planner":
    show_diet()

elif page == "📊 Dashboard":
    show_dashboard()

elif page == "ℹ️ About":
    show_about()
