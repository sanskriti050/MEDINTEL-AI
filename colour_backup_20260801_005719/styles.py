"""MedIntel AI visual theme — accessible light workspace + dark-teal sidebar."""
import streamlit as st


def load_css():
    st.markdown(
        """
        <style>
        :root {
            --mi-teal: #238878;
            --mi-sky: #4CA9EE;
            --mi-mint: #5ECD81;
            --mi-grey: #B2B7BB;
            --mi-ink: #163B36;
            --mi-muted: #486560;
            --mi-page: #F4FAF9;
            --mi-surface: #FFFFFF;
            --mi-line: #D7E5E1;
        }

        /* Main application: pale surfaces always carry dark copy. */
        .stApp { background: var(--mi-page); color: var(--mi-ink); }

        /* The earlier palette script changed both backgrounds AND text to the
           same four values. These rules restore readable contrast, including
           existing HTML cards whose colours are written inline in the pages. */
        .stApp, .stApp p, .stApp label, .stApp span, .stApp li,
        .stApp div[data-testid="stMarkdownContainer"],
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
            color: var(--mi-ink) !important;
        }
        /* Blue, mint, and grey are light surfaces: use dark text. */
        .stApp div[style*="#4CA9EE" i], .stApp div[style*="#5ECD81" i],
        .stApp div[style*="#B2B7BB" i] { color: var(--mi-ink) !important; }
        .stApp div[style*="#4CA9EE" i] *, .stApp div[style*="#5ECD81" i] *,
        .stApp div[style*="#B2B7BB" i] * { color: var(--mi-ink) !important; }
        /* Teal is the one dark palette surface: use white text. */
        .stApp div[style*="background:#238878" i],
        .stApp div[style*="background: #238878" i] { color: #FFFFFF !important; }
        .stApp div[style*="background:#238878" i] *,
        .stApp div[style*="background: #238878" i] * { color: #FFFFFF !important; }

        /* Hide Streamlit's automatic multipage list; navigation is rendered once below. */
        div[data-testid="stSidebarNav"] { display: none; }

        /* Controls and ordinary Streamlit surfaces. */
        div[data-testid="stMetric"], div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--mi-surface); border: 1px solid var(--mi-line);
            border-radius: 15px; padding: 12px;
            box-shadow: 0 2px 10px rgba(22, 59, 54, .05);
        }
        div[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 18px; padding: 15px; }
        .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] > div,
        .stNumberInput input, [data-testid="stFileUploader"] section {
            background: #FFFFFF !important; color: var(--mi-ink) !important;
            border-color: var(--mi-grey) !important;
        }
        .stButton > button {
            background: var(--mi-teal); color: #FFFFFF; border: 1px solid var(--mi-teal);
            border-radius: 10px; font-weight: 650; min-height: 44px;
        }
        .stButton > button:hover { background: #176C60; border-color: #176C60; color: #FFFFFF; }
        .stTabs [data-baseweb="tab"] { color: var(--mi-muted); }
        .stTabs [aria-selected="true"] { color: var(--mi-teal) !important; border-bottom-color: var(--mi-teal) !important; }

        /* The supplied custom sidebar: a dark-teal field uses light copy; its pale cards use ink. */
        section[data-testid="stSidebar"] {
            background: var(--mi-teal); border-right: 1px solid #176C60;
        }
        section[data-testid="stSidebar"] > div:first-child { padding-top: 1.1rem; }
        section[data-testid="stSidebar"] .medintel-title,
        section[data-testid="stSidebar"] .medintel-title span,
        section[data-testid="stSidebar"] .medintel-tagline,
        section[data-testid="stSidebar"] .medintel-intro,
        section[data-testid="stSidebar"] .sidebar-section-label { color: #FFFFFF !important; }
        section[data-testid="stSidebar"] .medintel-logo {
            background: var(--mi-sky) !important; box-shadow: 0 7px 18px rgba(10, 62, 54, .25) !important;
        }
        section[data-testid="stSidebar"] .sidebar-rule { background: rgba(255,255,255,.35) !important; }
        section[data-testid="stSidebar"] div[role="radiogroup"] { gap: 5px; }
        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            background: #EAF7F0 !important; border: 1px solid #BDE0CF !important;
            border-radius: 10px; padding: 8px 10px; min-height: 0;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label p {
            color: var(--mi-ink) !important; font-size: .82rem; font-weight: 650;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background: #D8F0E1 !important; border-color: var(--mi-mint) !important;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
            background: var(--mi-sky) !important; border-color: var(--mi-sky) !important;
            box-shadow: 0 5px 13px rgba(10, 62, 54, .2) !important;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p { color: #102F2A !important; }
        section[data-testid="stSidebar"] .sidebar-feature,
        section[data-testid="stSidebar"] .sidebar-disclaimer {
            background: #EAF7F0 !important; border: 1px solid #BDE0CF !important;
            border-radius: 10px;
        }
        section[data-testid="stSidebar"] .sidebar-feature b,
        section[data-testid="stSidebar"] .sidebar-feature small,
        section[data-testid="stSidebar"] .sidebar-disclaimer { color: var(--mi-ink) !important; }
        section[data-testid="stSidebar"] .sidebar-disclaimer { padding: 10px; margin-top: 9px; }
        </style>
        """,
        unsafe_allow_html=True,
    )
