import streamlit as st


def feature_card(icon: str, title: str, description: str):
    """Render a styled feature card."""
    st.markdown(f"""
    <div style="
        background:#172033;
        border:1px solid #2B3648;
        border-radius:16px;
        padding:20px;
        margin-bottom:12px;
        text-align:center;
    ">
        <div style="font-size:2rem;">{icon}</div>
        <h4 style="color:white;margin:8px 0 4px 0;">{title}</h4>
        <p style="color:#CBD5E1;font-size:0.9rem;margin:0;">{description}</p>
    </div>
    """, unsafe_allow_html=True)


def metric_card(title: str, value: str, icon: str = "📊", color: str = "#2563EB"):
    """Render a metric card with a colored accent."""
    st.markdown(f"""
    <div style="
        background:#172033;
        border:1px solid {color};
        border-radius:14px;
        padding:16px;
        text-align:center;
        margin-bottom:10px;
    ">
        <div style="font-size:1.8rem;">{icon}</div>
        <h3 style="color:white;margin:6px 0 2px 0;">{value}</h3>
        <p style="color:#94A3B8;font-size:0.85rem;margin:0;">{title}</p>
    </div>
    """, unsafe_allow_html=True)


def alert_card(message: str, level: str = "info"):
    """Render an alert card. level: info | warning | error | success"""
    colors = {
        "info": ("#1E3A5F", "#60A5FA"),
        "warning": ("#451A03", "#FCD34D"),
        "error": ("#450A0A", "#F87171"),
        "success": ("#052E16", "#4ADE80"),
    }
    bg, border = colors.get(level, colors["info"])

    st.markdown(f"""
    <div style="
        background:{bg};
        border-left:4px solid {border};
        border-radius:8px;
        padding:14px 18px;
        margin-bottom:10px;
    ">
        <p style="color:white;margin:0;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
