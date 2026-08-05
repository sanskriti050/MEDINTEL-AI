"""
Reusable card components for MedIntel AI.
All cards follow the warm earth-tone palette used across the app.
"""

import streamlit as st


def feature_card(icon: str, title: str, description: str, accent_color: str = "#4EBD8C"):
    """Render a styled feature card with a coloured top border."""
    st.markdown(
        f"""
        <div style="
            background:#ffffff;
            border:1px solid rgba(103, 177, 141, 0.20);
            border-top:3px solid {accent_color};
            border-radius:16px;
            padding:20px 18px;
            height:180px;
            margin-bottom:18px;
            box-shadow: 0 18px 36px rgba(80, 140, 95, 0.07);
        ">
            <div style="font-size:1.9rem;margin-bottom:10px;">{icon}</div>
            <h4 style="color:#1d4434;margin:0 0 10px 0;font-size:1.05rem;">{title}</h4>
            <p style="color:#4b5f4d;font-size:0.88rem;margin:0;line-height:1.7;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(title: str, value: str, subtitle: str = "", icon: str = "📊",
                color: str = "#C4956A"):
    """Render a stat/metric card."""
    st.markdown(
        f"""
        <div style="
            background:#fff8f0;
            border:1px solid rgba(204, 155, 100, 0.35);
            border-radius:16px;
            padding:18px 14px;
            text-align:center;
            box-shadow: 0 18px 36px rgba(156, 103, 55, 0.07);
        ">
            <div style="font-size:1.8rem;">{icon}</div>
            <h2 style="color:#5d4028;margin:6px 0 2px 0;font-size:1.6rem;">{value}</h2>
            <p style="color:#6c523f;font-size:0.9rem;font-weight:600;margin:0 0 2px 0;">{title}</p>
            <p style="color:#8a6a4b;font-size:0.78rem;margin:0;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def alert_card(message: str, level: str = "info"):
    """
    Render an inline alert banner.
    level: "info" | "warning" | "error" | "success"
    """
    styles = {
        "info":    {"bg": "#f0fbf4", "border": "#7ecfa0", "color": "#1f4733"},
        "warning": {"bg": "#fdf8ec", "border": "#d4a838", "color": "#5a3d00"},
        "error":   {"bg": "#fdf0ef", "border": "#c96e68", "color": "#5a1f1a"},
        "success": {"bg": "#f0fbf4", "border": "#4CAF82", "color": "#1a3d2b"},
    }
    s = styles.get(level, styles["info"])
    st.markdown(
        f"""
        <div style="
            background:{s['bg']};
            border-left:4px solid {s['border']};
            border-radius:8px;
            padding:14px 18px;
            margin-bottom:10px;
        ">
            <p style="color:{s['color']};margin:0;font-size:0.95rem;">{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def how_it_works_card(step_number: str, color: str, title: str, description: str):
    """Render a single 'How It Works' step card."""
    st.markdown(
        f"""
        <div style="
            background:#f7faf6;
            border:1px solid rgba(112, 182, 130, 0.22);
            border-radius:16px;
            padding:22px 16px;
            text-align:center;
            margin-bottom:8px;
            box-shadow:0 16px 30px rgba(80, 139, 103, 0.06);
        ">
            <div style="font-size:2rem;">{step_number}</div>
            <h4 style="color:{color};margin:8px 0 6px 0;font-size:0.95rem;">{title}</h4>
            <p style="color:#2f5140;font-size:0.85rem;margin:0;line-height:1.6;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
