import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
from datetime import datetime


# ── Health tips pool ─────────────────────────────────────────────────────────
HEALTH_TIPS = [
    ("💧", "Hydration",    "Drink 8–10 glasses of water daily. Dehydration causes fatigue, headaches, and poor concentration."),
    ("🥗", "Nutrition",    "Fill half your plate with vegetables and fruits. They provide essential vitamins, minerals, and fiber."),
    ("🏃", "Exercise",     "Walk 30 minutes daily. Even light exercise reduces the risk of heart disease, diabetes, and depression."),
    ("😴", "Sleep",        "Sleep 7–9 hours every night. Poor sleep is linked to weight gain, weak immunity, and mood disorders."),
    ("🧘", "Stress",       "Practice 10 minutes of deep breathing or meditation daily to lower cortisol and blood pressure."),
    ("🌞", "Vitamin D",    "Get 15–20 minutes of sunlight daily. Low Vitamin D is linked to weak bones and immune problems."),
    ("🫀", "Heart Health", "Reduce salt and saturated fats. High sodium increases blood pressure and risk of stroke."),
    ("🦷", "Oral Health",  "Brush twice daily and floss. Poor oral health is linked to heart disease and diabetes."),
    ("🩺", "Check-ups",    "Get a full body check-up every year, even if you feel healthy. Early detection saves lives."),
    ("🚭", "Avoid Smoke",  "Smoking damages every organ. Even passive smoke increases cancer and heart disease risk significantly."),
]

FEATURES = [
    ("📄", "Report Analyzer",   "Upload any blood test, thyroid, lipid, kidney, liver or X-ray PDF and get instant AI analysis.", "#4EBD8C"),
    ("🩺", "Symptom Checker",   "Describe your symptoms and get possible diagnoses, severity, home remedies and doctor recommendations.", "#6BC49D"),
    ("💊", "Medicine Guide",    "Search any medicine — Indian or international — and get complete dosage, side effects and interaction info.", "#78C8AA"),
    ("🥗", "Diet Planner",      "Get a personalized meal plan based on your age, weight, health goal and existing medical conditions.", "#47A56F"),
    ("📊", "Health Dashboard",  "Visualize your health score trends, report history and key health metrics all in one place.", "#3F9060"),
    ("ℹ️",  "About",            "Learn about the technology powering MedIntel AI and important usage disclaimers.", "#66B08A"),
]

STATS = [
    ("📄", "Report Types",   "15+",  "Blood, Thyroid, Lipid, Kidney, Liver & more"),
    ("🤖", "AI Model",       "LLaMA 3.3", "70B parameters via Groq"),
    ("⚡", "Analysis Speed", "~15s",  "Average report analysis time"),
    ("🌐", "Medicines",      "Any",   "Indian & international brands supported"),
]


def _tip_of_the_day():
    """Pick a consistent tip for today using date as seed."""
    random.seed(datetime.now().day + datetime.now().month)
    return random.choice(HEALTH_TIPS)


def show_home():

    # ── Hero Section ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="mi-hero" style="
        background: linear-gradient(135deg, #fff7ef 0%, #f4deca 45%, #e8c8a8 100%);
        border: 1px solid rgba(167, 102, 55, 0.24);
        border-radius: 24px;
        padding: 50px 40px 42px 40px;
        text-align: center;
        margin-bottom: 12px;
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position:absolute;top:0;left:0;right:0;bottom:0;
            background: radial-gradient(ellipse at 30% 50%, rgba(197, 236, 212, 0.34) 0%, transparent 55%),
                        radial-gradient(ellipse at 70% 50%, rgba(220, 244, 228, 0.30) 0%, transparent 58%);
            pointer-events:none;
        "></div>
        <div style="font-size:3.5rem;margin-bottom:12px;">🏥</div>
        <h1 class="mi-hero-title" style="
            color: #19462f !important;
            font-size: 3rem;
            font-weight: 800;
            margin: 0 0 12px 0;
            letter-spacing: -0.4px;
        ">MedIntel AI</h1>
        <p style="
            color: #2d533f;
            font-size: 1.2rem;
            margin: 0 0 24px 0;
            font-weight: 500;
        ">Your AI-Powered Intelligent Healthcare Assistant</p>
        <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
            <span style="background:rgba(229, 191, 148, 0.36);color:#6a4c30;padding:7px 16px;border-radius:22px;font-size:0.88rem;border:1px solid rgba(229, 191, 148, 0.45);">🤖 Groq LLaMA 3.3 70B</span>
            <span style="background:rgba(236, 204, 164, 0.36);color:#6a4c30;padding:7px 16px;border-radius:22px;font-size:0.88rem;border:1px solid rgba(236, 204, 164, 0.45);">⚡ Real-time Analysis</span>
            <span style="background:rgba(236, 206, 168, 0.32);color:#6a4c30;padding:7px 16px;border-radius:22px;font-size:0.88rem;border:1px solid rgba(236, 206, 168, 0.45);">🔒 Privacy First</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Quick Stats ──────────────────────────────────────────────────────────
    cols = st.columns(4)
    for i, (icon, label, value, sub) in enumerate(STATS):
        with cols[i]:
            st.markdown(f"""
            <div style="
                background:#fff8f0;border:1px solid rgba(204, 155, 100, 0.35);border-radius:16px;
                padding:18px 14px;text-align:center;
                box-shadow: 0 18px 36px rgba(156, 103, 55, 0.07);
            ">
                <div style="font-size:1.8rem;">{icon}</div>
                <h2 style="color:#5d4028;margin:6px 0 2px 0;font-size:1.6rem;">{value}</h2>
                <p style="color:#6c523f;font-size:0.9rem;font-weight:600;margin:0 0 2px 0;">{label}</p>
                <p style="color:#8a6a4b;font-size:0.78rem;margin:0;">{sub}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── Health Score Gauge + Welcome ─────────────────────────────────────────
    left, right = st.columns([1, 1])

    with left:
        st.subheader("📊 Sample Health Overview")

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=87,
            delta={"reference": 80, "valueformat": ".0f", "increasing": {"color": "#398463"}},
            title={"text": "Health Score", "font": {"color": "#5d4028", "size": 16}},
            number={"font": {"color": "#5d4028", "size": 44}, "suffix": "/100"},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#8b5d3d", "tickfont": {"color": "#8b5d3d"}},
                "bar": {"color": "#c48e5c", "thickness": 0.25},
                "bgcolor": "#fbf0e4",
                "bordercolor": "rgba(186, 134, 84, 0.26)",
                "steps": [
                    {"range": [0, 40],  "color": "#f2e3d1"},
                    {"range": [40, 70], "color": "#e7d0b4"},
                    {"range": [70, 100], "color": "#d9b58e"}
                ],
                "threshold": {
                    "line": {"color": "#ad7a49", "width": 3},
                    "thickness": 0.75,
                    "value": 87
                }
            }
        ))
        fig.update_layout(
            height=280,
            margin=dict(t=40, b=0, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Mini metrics row
        m1, m2, m3 = st.columns(3)
        m1.metric("❤️ Risk", "Low", "Stable")
        m2.metric("🩸 Abnormal", "2", "-1 this week")
        m3.metric("📄 Reports", "12", "+3")

    with right:
        st.subheader("👋 Welcome to MedIntel AI")
        st.markdown("""
        <div style="color:#1e4733;font-size:1rem;line-height:1.8;">
        MedIntel AI uses advanced artificial intelligence to help you understand your health better — without the jargon.
        <br><br>
        Whether you have a <b style="color:#4f9f79;">blood report</b> you don't understand, 
        <b style="color:#4a9e76;">symptoms</b> you're worried about, or want to know about a 
        <b style="color:#4f9f79;">medicine</b> your doctor prescribed — we've got you covered.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Health trend mini chart
        st.caption("📈 Sample Weekly Health Score Trend")
        trend_data = pd.DataFrame({
            "Week": ["W1", "W2", "W3", "W4", "W5", "W6"],
            "Score": [72, 75, 78, 80, 85, 87]
        })
        trend_fig = px.line(
            trend_data, x="Week", y="Score",
            markers=True,
            color_discrete_sequence=["#68b788"]
        )
        trend_fig.update_traces(
            line=dict(width=3),
            marker=dict(size=8, color="#92d4a5")
        )
        trend_fig.update_layout(
            height=200,
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(range=[60, 100], gridcolor="#b7dec8", tickfont=dict(color="#1f3c2f")),
            xaxis=dict(gridcolor="#b7dec8", tickfont=dict(color="#1f3c2f")),
            font=dict(color="#1f3c2f"),
            showlegend=False
        )
        st.plotly_chart(trend_fig, use_container_width=True)

    st.divider()

    # ── Features Grid ────────────────────────────────────────────────────────
    st.subheader("🚀 What Can MedIntel AI Do?")
    st.markdown("<div style='margin-top:32px;'></div>", unsafe_allow_html=True)

    row1 = st.columns([0.12, 0.94, 0.94])
    row2 = st.columns([0.12, 0.94, 0.94])
    row3 = st.columns([0.12, 0.94, 0.94])

    all_cols = row1[1:] + row2[1:] + row3[1:]
    for i, (icon, title, desc, color) in enumerate(FEATURES):
        with all_cols[i]:
            st.markdown(f"""
            <div style="
                background:#ffffff;
                border:1px solid rgba(103, 177, 141, 0.20);
                border-top:3px solid {color};
                border-radius:16px;
                padding:20px 18px;
                height:180px;
                margin-bottom:18px;
                box-shadow: 0 18px 36px rgba(80, 140, 95, 0.07);
            ">
                <div style="font-size:1.9rem;margin-bottom:10px;">{icon}</div>
                <h4 style="color:#1d4434;margin:0 0 10px 0;font-size:1.05rem;">{title}</h4>
                <p style="color:#4b5f4d;font-size:0.88rem;margin:0;line-height:1.7;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── How It Works ────────────────────────────────────────────────────────
    st.subheader("⚙️ How It Works")
    st.markdown("<br>", unsafe_allow_html=True)

    h1, h2, h3, h4 = st.columns(4)
    steps = [
        ("1️⃣", "#4EBD8C", "Upload / Input",    "Upload a PDF report, type symptoms, or search a medicine name"),
        ("2️⃣", "#6BC49D", "AI Processes",       "Groq's LLaMA 3.3 70B model analyzes your input in real-time"),
        ("3️⃣", "#78C8AA", "Get Insights",        "Receive health scores, diagnoses, recommendations, and advice"),
        ("4️⃣", "#47A56F", "Take Action",          "Download your report, follow diet tips, or consult your doctor"),
    ]
    for col, (num, color, title, desc) in zip([h1, h2, h3, h4], steps):
        with col:
            st.markdown(f"""
            <div style="background:#f7faf6;border:1px solid rgba(112, 182, 130, 0.22);border-radius:16px;padding:22px 16px;text-align:center;margin-bottom:8px;box-shadow:0 16px 30px rgba(80, 139, 103, 0.06);">
                <div style="font-size:2rem;">{num}</div>
                <h4 style="color:{color};margin:8px 0 6px 0;font-size:0.95rem;">{title}</h4>
                <p style="color:#2f5140;font-size:0.85rem;margin:0;line-height:1.6;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── Tip of the Day ───────────────────────────────────────────────────────
    tip_icon, tip_cat, tip_text = _tip_of_the_day()
    st.subheader("💡 Health Tip of the Day")
    st.markdown(f"""
    <div style="
        background:#f2fbf3;
        border: 1px solid rgba(102, 196, 143, 0.30);
        border-radius: 16px;
        padding: 24px 28px;
    ">
        <div style="display:flex;align-items:center;gap:14px;">
            <div style="font-size:2.5rem;">{tip_icon}</div>
            <div>
                <p style="color:#2c5d43;font-size:0.85rem;font-weight:700;margin:0 0 4px 0;text-transform:uppercase;letter-spacing:1px;">{tip_cat}</p>
                <p style="color:#21513d;font-size:1.05rem;margin:0;line-height:1.6;">{tip_text}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── Disclaimer ───────────────────────────────────────────────────────────
    st.markdown("""
    <div style="
        background:#eff9ef;border:1px solid rgba(115, 189, 129, 0.32);border-radius:14px;
        padding:16px 20px;text-align:center;
    ">
        <p style="color:#224835;font-size:0.9rem;margin:0;">
        ⚠️ <b>Medical Disclaimer:</b> MedIntel AI is for <b>informational purposes only</b> and does <b>not</b> replace professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.
        </p>
    </div>
    """, unsafe_allow_html=True)
