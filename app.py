import streamlit as st

from pages.home import show_home
from pages.report import show_report
from pages.symptom import show_symptom
from pages.medicine import show_medicine
from pages.diet import show_diet
from pages.dashboard import show_dashboard
from pages.about import show_about
from styles import load_css

st.set_page_config(
    page_title="MedIntel AI",
    page_icon="🏥",
    layout="wide"
)
load_css()

st.sidebar.markdown("""<div class="mi-side-brand"><div>✦</div><span>MEDINTEL <b>AI</b></span><small>INTELLIGENT HEALTHCARE</small></div>""", unsafe_allow_html=True)
st.sidebar.markdown("<p class='mi-side-label'>EXPLORE YOUR HEALTH</p>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📄 Report Analyzer",
        "🩺 Symptom Checker",
        "💊 Medicine Guide",
        "🥗 Diet Planner",
        "📊 Dashboard",
        "ℹ About"
    ]
)


st.sidebar.markdown("""<div class="mi-side-footer">🔒 Your health journey, kept simple.<br><span>Information, not a medical diagnosis.</span></div>""", unsafe_allow_html=True)

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

elif page == "ℹ About":
    show_about()