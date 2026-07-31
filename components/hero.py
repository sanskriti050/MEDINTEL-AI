import streamlit as st


def show_hero(title: str, subtitle: str, badge: str = ""):
    """Render a premium informational page header; it does not change app behavior."""
    badge_html = f'<span class="mi-eyebrow">{badge}</span>' if badge else '<span class="mi-eyebrow">MEDINTEL AI</span>'
    st.markdown(f"""
    <section class="mi-hero">
        <div class="mi-hero-glow"></div>
        <div class="mi-hero-copy">
            {badge_html}
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        <div class="mi-hero-orb">✦</div>
    </section>
    """, unsafe_allow_html=True)


def show_page_header(icon: str, title: str, subtitle: str = ""):
    show_hero(f"{icon} {title}", subtitle)


def show_notice(title: str, text: str, icon: str = "✦"):
    st.markdown(f"""
    <div class="mi-notice"><span>{icon}</span><div><b>{title}</b><p>{text}</p></div></div>
    """, unsafe_allow_html=True)
