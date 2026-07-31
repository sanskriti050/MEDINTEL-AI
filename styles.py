import streamlit as st

def load_css():
    st.markdown("""
    <style>

    .stApp{
        background-color:#0B1220;
    }

    section[data-testid="stSidebar"]{
        background:#111827;
        border-right:1px solid #334155;
    }

    h1,h2,h3,h4,h5,h6{
        color:white !important;
    }

    /* Keep normal Streamlit text readable without overriding colours used inside custom UI cards. */
    div[data-testid="stMarkdownContainer"] > p,
    div[data-testid="stWidgetLabel"] > label{
        color:#CBD5E1 !important;
    }

    /* Streamlit places button labels inside nested elements; force every action label to white. */
    .stButton > button,
    .stFormSubmitButton > button,
    .stDownloadButton > button,
    div[data-testid="stButton"] > button,
    div[data-testid="stFormSubmitButton"] > button{
        background:#2563EB !important;
        color:#FFFFFF !important;
        border-radius:10px;
        border:none;
        font-weight:600;
        height:48px;
    }

    .stButton > button *,
    .stFormSubmitButton > button *,
    .stDownloadButton > button *,
    div[data-testid="stButton"] > button *,
    div[data-testid="stFormSubmitButton"] > button *{
        color:#FFFFFF !important;
        opacity:1 !important;
    }

    div[data-testid="stMetric"]{
        background:#172033;
        border-radius:15px;
        padding:12px;
        border:1px solid #2B3648;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]{
        background:#172033;
        border-radius:18px;
        border:1px solid #2B3648;
        padding:15px;
    }

    .stButton>button{
        background:#2563EB;
        color:white;
        border-radius:10px;
        border:none;
        font-weight:600;
        height:48px;
    }

    .stButton>button:hover,
    .stFormSubmitButton>button:hover,
    .stDownloadButton>button:hover{
        background:#1D4ED8 !important;
    }

    </style>
    """, unsafe_allow_html=True)