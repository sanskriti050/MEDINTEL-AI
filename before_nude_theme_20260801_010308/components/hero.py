import streamlit as st


def show_hero(title: str, subtitle: str, badge: str = ""):
    """Render a hero section with title and subtitle."""
    badge_html = f'<span style="background:#2563EB;color:white;padding:4px 12px;border-radius:20px;font-size:0.8rem;font-weight:600;">{badge}</span>' if badge else ""

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #0B1220 0%, #172033 100%);
        border: 1px solid #2B3648;
        border-radius: 20px;
        padding: 40px 30px;
        text-align: center;
        margin-bottom: 24px;
    ">
        {badge_html}
        <h1 style="color:white;margin:16px 0 8px 0;font-size:2.4rem;">{title}</h1>
        <p style="color:#94A3B8;font-size:1.1rem;margin:0;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def show_page_header(icon: str, title: str, subtitle: str = ""):
    """Render a simple page header with icon."""
    st.markdown(f"""
    <div style="margin-bottom:16px;">
        <h1 style="color:white;margin-bottom:4px;">{icon} {title}</h1>
        {'<p style="color:#94A3B8;margin:0;">' + subtitle + '</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)
