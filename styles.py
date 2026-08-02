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
    /* remove any default page margins/stripe and hide Streamlit header bar */
    html, body, #root, .main, .block-container {
        background: var(--warm-bg) !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    header, [data-testid="stHeader"], [data-testid="stToolbar"], [role="banner"] {
        display: none !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    section[data-testid="stSidebar"], div[role="complementary"], div[data-testid="stSidebarNav"] {
        background: #C8956C !important;
        background-image: none !important;
        border-right:1px solid #A8724A !important;
        width: 240px !important;
        min-width: 240px !important;
        max-width: 240px !important;
    }
    section[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] > div:first-child,
    [data-testid="stSidebarContent"] {
        background: #C8956C !important;
        background-image: none !important;
    }
    section[data-testid="stSidebar"] * { color:#FFF3E8 !important; font-size: 0.95rem !important; }
    section[data-testid="stSidebar"] .stRadio label { 
        border-radius: 8px !important;
        padding: 8px 10px !important;
        margin-bottom: 4px !important;
        font-size: 0.95rem !important;
    }
    section[data-testid="stSidebar"] .stRadio label:hover { 
        background: rgba(180,130,80,0.15) !important;
    }
    h1,h2,h3,h4,h5,h6 { color:var(--ink) !important; }
    p,label,span { color:var(--muted) !important; }
    .stMarkdown,.stText,[data-testid="stWidgetLabel"] { color:var(--ink); }
    div[data-testid="stMetric"],div[data-testid="stVerticalBlockBorderWrapper"] { background:var(--warm-surface); border:1px solid var(--warm-border); border-radius:16px; padding:14px; box-shadow:0 8px 24px rgba(73,57,39,.06); }
    [data-testid="stMetricLabel"] p { color:var(--muted) !important; }
    [data-testid="stMetricValue"] { color:var(--green-deep); }
    .stButton > button { background:#C4956A; color:#FFF8EB !important; border:1px solid #B5845A; border-radius:10px; font-weight:650; height:46px; transition:all .18s ease; }
    .stButton > button:hover { background:#A97548; border-color:#9A6840; transform:translateY(-1px); }
    .stFormSubmitButton > button { background:#C4956A !important; color:#FFF8EB !important; border:1px solid #B5845A !important; border-radius:10px !important; font-weight:650 !important; height:46px !important; transition:all .18s ease !important; }
    .stFormSubmitButton > button:hover { background:#A97548 !important; border-color:#9A6840 !important; transform:translateY(-1px) !important; }
    .stDownloadButton > button { background:#C4956A !important; color:#FFF8EB !important; border:1px solid #B5845A !important; border-radius:10px !important; font-weight:650 !important; height:46px !important; transition:all .18s ease !important; }
    .stDownloadButton > button:hover { background:#A97548 !important; border-color:#9A6840 !important; transform:translateY(-1px) !important; }
    div[data-baseweb="input"] > div,div[data-baseweb="select"] > div,textarea { background:#FFF7E9 !important; border-color:var(--warm-border) !important; color:var(--ink) !important; }
    [data-testid="stFileUploader"] { background:rgba(246,238,223,.72); border-radius:14px; border:1px dashed #A98F70; padding:8px; }
    hr { border-color:var(--warm-border) !important; }
    .block-container { padding: 24px 28px 28px 28px !important; max-width: 1400px; margin: 0 auto; }
    section[data-testid="stSidebar"] { padding: 22px 18px 20px 18px; width: 240px !important; max-width: 240px !important; min-width: 240px !important; }
    .stApp, .main, .block-container, .stMarkdown, .stText, .stTextArea, .stSelectbox { line-height: 1.6 !important; }
    [data-testid="stAppViewContainer"], #root > div, #root > div > div, #root > div > div > div, .main {
        background: var(--warm-bg) !important;
        border-radius: 0 !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
