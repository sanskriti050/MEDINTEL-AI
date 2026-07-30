import streamlit as st

def load_css():
    st.markdown("""
    <style>
    /* Keep the main application exactly as it was */
    .stApp { background-color: #0B1220; }

    /* Sidebar matching the supplied reference */
    section[data-testid="stSidebar"] {
        background: #141725;
        border-right: 1px solid #2A2E40;
    }
    section[data-testid="stSidebar"] > div:first-child { padding-top: 2.5rem; }
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] { padding: 0 0.65rem; }

    .sidebar-brand { padding: 0.55rem 0.05rem 0.7rem; }
    .sidebar-brand h2 {
        margin: 0;
        color: #F7F7FC !important;
        font-size: 1.12rem;
        font-weight: 750;
        letter-spacing: -0.035em;
    }
    .sidebar-brand p {
        margin: 0.7rem 0 0;
        color: #A8AEC5 !important;
        font-size: 0.62rem;
        line-height: 1.55;
    }
    .sidebar-rule { border: 0; border-top: 1px solid #303448; margin: 0.15rem 0 0.85rem; }
    .sidebar-section-title {
        color: #9CA3BD !important;
        font-size: 0.54rem;
        font-weight: 800;
        letter-spacing: 0.09em;
        margin: 0 0 0.52rem;
    }

    /* The radio's own label is visually hidden; individual choices stay visible. */
    section[data-testid="stSidebar"] [data-testid="stRadio"] > label {
        display: none;
    }
    section[data-testid="stSidebar"] [role="radiogroup"] {
        gap: 0.62rem;
    }
    section[data-testid="stSidebar"] [role="radiogroup"] label {
        background: #1B1F31;
        border: 1px solid #2D334A;
        border-radius: 0.5rem;
        min-height: 2.25rem;
        padding: 0.1rem 0.6rem;
        color: #DCE0F0 !important;
        font-size: 0.68rem;
        font-weight: 650;
        transition: background 150ms ease, border-color 150ms ease, transform 150ms ease;
    }
    section[data-testid="stSidebar"] [role="radiogroup"] label p,
    section[data-testid="stSidebar"] [role="radiogroup"] label span {
        color: #DCE0F0 !important;
        font-size: 0.68rem !important;
        font-weight: 650;
    }
    section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: #252B42;
        border-color: #4D5FA6;
        transform: translateX(1px);
    }
    section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg, #6479E7 0%, #4C62D5 100%);
        border-color: #7186F3;
        box-shadow: 0 5px 13px rgba(65, 83, 190, 0.28);
    }
    section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p,
    section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) span {
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] [role="radiogroup"] input { accent-color: #4758BC; }

    /* Original main-content styling */
    h1,h2,h3,h4,h5,h6 { color: white !important; }
    p,label,span { color: #CBD5E1 !important; }
    div[data-testid="stMetric"] {
        background: #172033; border-radius: 15px; padding: 12px; border: 1px solid #2B3648;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #172033; border-radius: 18px; border: 1px solid #2B3648; padding: 15px;
    }
    .stButton>button {
        background: #2563EB; color: white; border-radius: 10px; border: none; font-weight: 600; height: 48px;
    }
    .stButton>button:hover { background: #1D4ED8; }
    </style>
    """, unsafe_allow_html=True)
