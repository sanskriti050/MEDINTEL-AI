import streamlit as st


def feature_card(icon: str, title: str, description: str):
    """Render a styled feature card."""
    st.markdown(f"""
    <div style="
        background:#B2B7BB;
        border:1px solid #238878;
        border-radius:16px;
        padding:20px;
        margin-bottom:12px;
        text-align:center;
    ">
        <div style="font-size:2rem;">{icon}</div>
        <h4 style="color:#3E2D27;margin:8px 0 4px 0;">{title}</h4>
        <p style="color:#238878;font-size:0.9rem;margin:0;">{description}</p>
    </div>
    """, unsafe_allow_html=True)


def metric_card(title: str, value: str, icon: str = "📊", color: str = "#4CA9EE"):
    """Render a metric card with a colored accent."""
    st.markdown(f"""
    <div style="
        background:#B2B7BB;
        border:1px solid {color};
        border-radius:14px;
        padding:16px;
        text-align:center;
        margin-bottom:10px;
    ">
        <div style="font-size:1.8rem;">{icon}</div>
        <h3 style="color:#3E2D27;margin:6px 0 2px 0;">{value}</h3>
        <p style="color:#238878;font-size:0.85rem;margin:0;">{title}</p>
    </div>
    """, unsafe_allow_html=True)


def alert_card(message: str, level: str = "info"):
    """Render an alert card. level: info | warning | error | success"""
    colors = {
        "info": ("#4CA9EE", "#4CA9EE"),
        "warning": ("#238878", "#238878"),
        "error": ("#238878", "#238878"),
        "success": ("#5ECD81", "#5ECD81"),
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
        <p style="color:#3E2D27;margin:0;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
