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

    p,label,span{
        color:#CBD5E1 !important;
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

    .stButton>button:hover{
        background:#1D4ED8;
    }

    </style>
    """, unsafe_allow_html=True)