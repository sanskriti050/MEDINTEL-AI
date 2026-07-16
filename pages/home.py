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
    ("📄", "Report Analyzer",   "Upload any blood test, thyroid, lipid, kidney, liver or X-ray PDF and get instant AI analysis.", "#2563EB"),
    ("🩺", "Symptom Checker",   "Describe your symptoms and get possible diagnoses, severity, home remedies and doctor recommendations.", "#7C3AED"),
    ("💊", "Medicine Guide",    "Search any medicine — Indian or international — and get complete dosage, side effects and interaction info.", "#059669"),
    ("🥗", "Diet Planner",      "Get a personalized meal plan based on your age, weight, health goal and existing medical conditions.", "#D97706"),
    ("📊", "Health Dashboard",  "Visualize your health score trends, report history and key health metrics all in one place.", "#DC2626"),
    ("ℹ️",  "About",            "Learn about the technology powering MedIntel AI and important usage disclaimers.", "#0891B2"),
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
    <div style="
        background: linear-gradient(135deg, #0f1f3d 0%, #1a2f5c 50%, #0f1f3d 100%);
        border: 1px solid #2563EB;
        border-radius: 20px;
        padding: 48px 36px 40px 36px;
        text-align: center;
        margin-bottom: 8px;
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position:absolute;top:0;left:0;right:0;bottom:0;
            background: radial-gradient(ellipse at 30% 50%, rgba(37,99,235,0.15) 0%, transparent 60%),
                        radial-gradient(ellipse at 70% 50%, rgba(124,58,237,0.1) 0%, transparent 60%);
            pointer-events:none;
        "></div>
        <div style="font-size:3.5rem;margin-bottom:12px;">🏥</div>
        <h1 style="
            color: white;
            font-size: 2.8rem;
            font-weight: 800;
            margin: 0 0 10px 0;
            letter-spacing: -0.5px;
        ">MedIntel AI</h1>
        <p style="
            color: #93C5FD;
            font-size: 1.2rem;
            margin: 0 0 20px 0;
            font-weight: 400;
        ">Your AI-Powered Intelligent Healthcare Assistant</p>
        <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
            <span style="background:rgba(37,99,235,0.3);color:#93C5FD;padding:6px 16px;border-radius:20px;font-size:0.85rem;border:1px solid #2563EB;">🤖 Groq LLaMA 3.3 70B</span>
            <span style="background:rgba(5,150,105,0.3);color:#6EE7B7;padding:6px 16px;border-radius:20px;font-size:0.85rem;border:1px solid #059669;">⚡ Real-time Analysis</span>
            <span style="background:rgba(124,58,237,0.3);color:#C4B5FD;padding:6px 16px;border-radius:20px;font-size:0.85rem;border:1px solid #7C3AED;">🔒 Privacy First</span>
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
                background:#172033;border:1px solid #2B3648;border-radius:14px;
                padding:18px 14px;text-align:center;
            ">
                <div style="font-size:1.8rem;">{icon}</div>
                <h2 style="color:#60A5FA;margin:6px 0 2px 0;font-size:1.6rem;">{value}</h2>
                <p style="color:white;font-size:0.9rem;font-weight:600;margin:0 0 2px 0;">{label}</p>
                <p style="color:#64748B;font-size:0.78rem;margin:0;">{sub}</p>
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
            delta={"reference": 80, "valueformat": ".0f", "increasing": {"color": "#16A34A"}},
            title={"text": "Health Score", "font": {"color": "white", "size": 16}},
            number={"font": {"color": "white", "size": 44}, "suffix": "/100"},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "white", "tickfont": {"color": "white"}},
                "bar": {"color": "#2563EB", "thickness": 0.25},
                "bgcolor": "#172033",
                "bordercolor": "#334155",
                "steps": [
                    {"range": [0, 40],  "color": "#450a0a"},
                    {"range": [40, 70], "color": "#451a03"},
                    {"range": [70, 100], "color": "#052e16"}
                ],
                "threshold": {
                    "line": {"color": "#16A34A", "width": 3},
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
        <div style="color:#CBD5E1;font-size:1rem;line-height:1.8;">
        MedIntel AI uses advanced artificial intelligence to help you understand your health better — without the jargon.
        <br><br>
        Whether you have a <b style="color:#60A5FA;">blood report</b> you don't understand, 
        <b style="color:#A78BFA;">symptoms</b> you're worried about, or want to know about a 
        <b style="color:#34D399;">medicine</b> your doctor prescribed — we've got you covered.
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
            color_discrete_sequence=["#2563EB"]
        )
        trend_fig.update_traces(
            line=dict(width=3),
            marker=dict(size=8, color="#60A5FA")
        )
        trend_fig.update_layout(
            height=200,
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(range=[60, 100], gridcolor="#1e293b", tickfont=dict(color="white")),
            xaxis=dict(gridcolor="#1e293b", tickfont=dict(color="white")),
            font=dict(color="white"),
            showlegend=False
        )
        st.plotly_chart(trend_fig, use_container_width=True)

    st.divider()

    # ── Features Grid ────────────────────────────────────────────────────────
    st.subheader("🚀 What Can MedIntel AI Do?")
    st.markdown("<br>", unsafe_allow_html=True)

    row1 = st.columns(3)
    row2 = st.columns(3)

    all_cols = row1 + row2
    for i, (icon, title, desc, color) in enumerate(FEATURES):
        with all_cols[i]:
            st.markdown(f"""
            <div style="
                background:#172033;
                border:1px solid #2B3648;
                border-top:3px solid {color};
                border-radius:14px;
                padding:20px 16px;
                height:160px;
                margin-bottom:12px;
            ">
                <div style="font-size:1.8rem;margin-bottom:8px;">{icon}</div>
                <h4 style="color:white;margin:0 0 6px 0;font-size:1rem;">{title}</h4>
                <p style="color:#94A3B8;font-size:0.82rem;margin:0;line-height:1.5;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── How It Works ────────────────────────────────────────────────────────
    st.subheader("⚙️ How It Works")
    st.markdown("<br>", unsafe_allow_html=True)

    h1, h2, h3, h4 = st.columns(4)
    steps = [
        ("1️⃣", "#2563EB", "Upload / Input",    "Upload a PDF report, type symptoms, or search a medicine name"),
        ("2️⃣", "#7C3AED", "AI Processes",       "Groq's LLaMA 3.3 70B model analyzes your input in real-time"),
        ("3️⃣", "#059669", "Get Insights",        "Receive health scores, diagnoses, recommendations, and advice"),
        ("4️⃣", "#D97706", "Take Action",          "Download your report, follow diet tips, or consult your doctor"),
    ]
    for col, (num, color, title, desc) in zip([h1, h2, h3, h4], steps):
        with col:
            st.markdown(f"""
            <div style="
                background:#172033;border:1px solid #2B3648;border-radius:14px;
                padding:20px 14px;text-align:center;margin-bottom:8px;
            ">
                <div style="font-size:2rem;">{num}</div>
                <h4 style="color:{color};margin:8px 0 6px 0;font-size:0.95rem;">{title}</h4>
                <p style="color:#94A3B8;font-size:0.8rem;margin:0;line-height:1.5;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── Tip of the Day ───────────────────────────────────────────────────────
    tip_icon, tip_cat, tip_text = _tip_of_the_day()
    st.subheader("💡 Health Tip of the Day")
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #052e16 0%, #0f2744 100%);
        border: 1px solid #16A34A;
        border-radius: 14px;
        padding: 24px 28px;
    ">
        <div style="display:flex;align-items:center;gap:14px;">
            <div style="font-size:2.5rem;">{tip_icon}</div>
            <div>
                <p style="color:#4ADE80;font-size:0.85rem;font-weight:700;margin:0 0 4px 0;text-transform:uppercase;letter-spacing:1px;">{tip_cat}</p>
                <p style="color:#D1FAE5;font-size:1.05rem;margin:0;line-height:1.6;">{tip_text}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── Disclaimer ───────────────────────────────────────────────────────────
    st.markdown("""
    <div style="
        background:#1c1207;border:1px solid #92400E;border-radius:12px;
        padding:16px 20px;text-align:center;
    ">
        <p style="color:#FCD34D;font-size:0.85rem;margin:0;">
        ⚠️ <b>Medical Disclaimer:</b> MedIntel AI is for <b>informational purposes only</b> and does <b>not</b> replace professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.
        </p>
    </div>
    """, unsafe_allow_html=True)
