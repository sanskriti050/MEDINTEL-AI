import streamlit as st


def load_css():
    """Apply a light warm-earth palette that complements the forest-green brand."""
    st.markdown("""
    <style>
    :root {
        --warm-bg: #E8DDC8;
        --warm-surface: #F6EEDF;
        --warm-border: #CDBB9F;
        --ink: #26382B;
        --muted: #625E4D;
        --green: #4C7655;
        --green-deep: #31533A;
    }
    .stApp {
        background: radial-gradient(circle at 85% 4%, rgba(129,154,112,.18), transparent 28%), radial-gradient(circle at 8% 92%, rgba(193,142,87,.13), transparent 30%), var(--warm-bg);
        color: var(--ink);
    }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg,var(--warm-surface) 0%, var(--warm-bg) 100%); border-right:1px solid var(--warm-border); }
    section[data-testid="stSidebar"] * { color:var(--muted) !important; }
    section[data-testid="stSidebar"] .stRadio label { border:1px solid rgba(240,225,201,.14); border-radius:10px; padding:8px 10px; margin-bottom:5px; }
    section[data-testid="stSidebar"] .stRadio label:hover { background:rgba(217,230,207,.14); border-color:rgba(217,230,207,.34); }
    h1,h2,h3,h4,h5,h6 { color:var(--ink) !important; }
    p,label,span { color:var(--muted) !important; }
    .stMarkdown,.stText,[data-testid="stWidgetLabel"] { color:var(--ink); }
    div[data-testid="stMetric"],div[data-testid="stVerticalBlockBorderWrapper"] { background:var(--warm-surface); border:1px solid var(--warm-border); border-radius:16px; padding:14px; box-shadow:0 8px 24px rgba(73,57,39,.06); }
    [data-testid="stMetricLabel"] p { color:var(--muted) !important; }
    [data-testid="stMetricValue"] { color:var(--green-deep); }
    .stButton > button { background:var(--green); color:#FFF8EB !important; border:1px solid var(--green); border-radius:10px; font-weight:650; height:46px; transition:all .18s ease; }
    .stButton > button:hover { background:var(--green-deep); border-color:var(--green-deep); transform:translateY(-1px); }
    div[data-baseweb="input"] > div,div[data-baseweb="select"] > div,textarea { background:#FFF7E9 !important; border-color:var(--warm-border) !important; color:var(--ink) !important; }
    [data-testid="stFileUploader"] { background:rgba(246,238,223,.72); border-radius:14px; border:1px dashed #A98F70; padding:8px; }
    hr { border-color:var(--warm-border) !important; }
    </style>
    """, unsafe_allow_html=True)
