import streamlit as st


def render_sidebar() -> str:
    """
    Render the full application sidebar — branding, navigation, RAG status,
    quick tip, and footer disclaimer.

    Returns
    -------
    str
        The currently selected page label (matches the radio options).
    """

    # ── Force sidebar background colour ──────────────────────────────────────
    st.markdown("""
    <style>
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] > div > div,
    [data-testid="stSidebarContent"],
    section[data-testid="stSidebar"] {
        background-color: #C8956C !important;
        background-image: none !important;
        background: #C8956C !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Branding header ───────────────────────────────────────────────────────
    st.sidebar.markdown("""
    <div style="padding: 24px 4px 8px 4px;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
            <div style="background:rgba(255,255,255,0.18); border-radius:10px; width:38px; height:38px;
                        display:flex; align-items:center; justify-content:center; font-size:1.3rem;">🏥</div>
            <div>
                <div style="color:#FFF8F0; font-size:1rem; font-weight:800;
                            letter-spacing:0.5px; line-height:1.2;">MedIntel AI</div>
                <div style="color:rgba(255,245,230,0.70); font-size:0.68rem;
                            letter-spacing:1.5px; text-transform:uppercase;
                            font-weight:500;">Healthcare Assistant</div>
            </div>
        </div>
        <div style="height:1px; background:rgba(255,255,255,0.15); margin:16px 0 14px 0;"></div>
        <div style="color:rgba(255,245,230,0.60); font-size:0.72rem; letter-spacing:1.8px;
                    text-transform:uppercase; font-weight:600; margin-bottom:10px;
                    padding-left:2px;">Navigation</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Navigation ────────────────────────────────────────────────────────────
    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Home",
            "📄 Report Analyzer",
            "🩺 Symptom Checker",
            "💊 Medicine Guide",
            "🥗 Diet Planner",
            "📊 Dashboard",
            "ℹ️ About",
        ],
        label_visibility="collapsed",
    )

    # ── RAG status indicator ──────────────────────────────────────────────────
    st.sidebar.markdown("""
    <div style="margin-top:16px; padding: 0 4px;">
        <div style="height:1px; background:rgba(255,255,255,0.15); margin-bottom:12px;"></div>
    </div>
    """, unsafe_allow_html=True)

    rag_html = ""
    try:
        from rag_engine import get_rag_status
        rag = get_rag_status()
        if rag["active"]:
            rag_html = (
                f"""<div style="background:rgba(80,200,120,0.15);border:1px solid rgba(80,200,120,0.35);"""
                f"""border-radius:10px;padding:10px 14px;margin-top:0;">"""
                f"""<div style="display:flex;align-items:center;gap:8px;">"""
                f"""<div style="width:8px;height:8px;border-radius:50%;background:#5EC87A;"""
                f"""box-shadow:0 0 6px #5EC87A;flex-shrink:0;"></div>"""
                f"""<div style="color:#DFFFEC;font-size:0.75rem;font-weight:700;">RAG Active</div>"""
                f"""</div>"""
                f"""<div style="color:rgba(220,255,235,0.65);font-size:0.68rem;margin-top:4px;line-height:1.4;">"""
                f"""{rag['chunks']} medical knowledge chunks &nbsp;|&nbsp; {rag['model']}</div></div>"""
            )
        else:
            rag_html = (
                """<div style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);"""
                """border-radius:10px;padding:10px 14px;">"""
                """<div style="display:flex;align-items:center;gap:8px;">"""
                """<div style="width:8px;height:8px;border-radius:50%;background:#aaa;flex-shrink:0;"></div>"""
                """<div style="color:rgba(255,245,230,0.5);font-size:0.75rem;">RAG Inactive</div></div>"""
                """<div style="color:rgba(255,245,230,0.4);font-size:0.68rem;margin-top:4px;">"""
                """pip install faiss-cpu sentence-transformers</div></div>"""
            )
    except Exception:
        pass

    if rag_html:
        st.sidebar.markdown(rag_html, unsafe_allow_html=True)

    # ── Quick tip + footer ────────────────────────────────────────────────────
    st.sidebar.markdown("""
    <div style="padding: 0 4px;">
        <div style="height:1px; background:rgba(255,255,255,0.15); margin:12px 0 10px 0;"></div>
        <div style="background:rgba(255,255,255,0.10); border-radius:10px;
                    padding:10px 14px; margin-bottom:12px;">
            <div style="color:#FFF8F0; font-size:0.75rem; font-weight:700;
                        margin-bottom:3px;">💡 Quick Tip</div>
            <div style="color:rgba(255,245,230,0.75); font-size:0.7rem; line-height:1.5;">
                Upload a PDF on <b style="color:#FFE8CC;">Report Analyzer</b>
                for instant AI analysis.
            </div>
        </div>
        <div style="color:rgba(255,245,230,0.45); font-size:0.66rem;
                    text-align:center; line-height:1.6;">
            🔒 For informational use only<br>Not a medical diagnosis
        </div>
    </div>
    """, unsafe_allow_html=True)

    return page
