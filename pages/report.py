import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json

from utils import extract_text_from_pdf, detect_report_type
from analyzer import analyze_medical_report
from dashboard_connector import save_report_to_dashboard


def show_report():

    st.title("📄 AI Medical Report Analyzer")
    st.caption("Upload any medical report PDF — CBC, Lipid, Thyroid, Kidney, Liver, Diabetes, Urine, Radiology, and more.")

    # ── Session state ────────────────────────────────────────
    for key in ("report_result", "report_text", "report_type", "last_filename"):
        if key not in st.session_state:
            st.session_state[key] = None

    # ── Upload ───────────────────────────────────────────────
    uploaded = st.file_uploader(
        "📤 Upload Medical Report (PDF only)",
        type=["pdf"],
        help="Supports text-based and scanned PDFs. Max recommended size: 10 MB."
    )

    if uploaded is None:
        st.info("👆 Upload a PDF medical report to get started.")
        # Clear previous results when file is removed
        for key in ("report_result", "report_text", "report_type", "last_filename"):
            st.session_state[key] = None
        return

    # Only re-extract if a new file was uploaded
    if uploaded.name != st.session_state.last_filename:
        st.session_state.report_result = None
        with st.spinner("📖 Reading PDF... If it's a scanned report, AI Vision will be used automatically (may take 15–30 seconds)..."):
            text = extract_text_from_pdf(uploaded)
        st.session_state.report_text = text
        st.session_state.report_type = detect_report_type(text)
        st.session_state.last_filename = uploaded.name

    text = st.session_state.report_text
    report_type = st.session_state.report_type

    if not text or not text.strip():
        st.error("❌ Could not extract text from this PDF automatically.")
        st.info("""
**Try these options:**

1. **Manual text paste** — Open your PDF, select all text (Ctrl+A), copy and paste it in the box below.
2. **Image PDF** — Take a screenshot of your report and describe the key values manually.
3. **Install Tesseract OCR** — For scanned PDFs, install [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and `pytesseract` for automatic OCR.
        """)

        st.subheader("✍️ Paste Report Text Manually")
        manual_text = st.text_area(
            "Paste your report text here:",
            placeholder="e.g.\nHemoglobin: 11.2 g/dL (Low)\nWBC: 6500 /uL\nCholesterol: 210 mg/dL (High)\n...",
            height=250,
            key="manual_report_text"
        )
        if st.button("🤖 Analyze Pasted Text", use_container_width=True, type="primary", key="analyze_manual"):
            if manual_text.strip():
                detected = detect_report_type(manual_text)
                st.session_state.report_text = manual_text
                st.session_state.report_type = detected
                with st.spinner("🧠 Analyzing your report..."):
                    result = analyze_medical_report(manual_text, detected)
                st.session_state.report_result = result
                # ── Auto-save to dashboard ──────────────────────────────
                if result.get("health_score", 0) > 0:
                    save_report_to_dashboard(result, detected, "manual-paste")
                st.rerun()
            else:
                st.warning("Please paste some text first.")
        return

    # ── Upload success banner ────────────────────────────────
    col_s, col_t = st.columns([3, 1])
    with col_s:
        st.success(f"✅ **{uploaded.name}** uploaded successfully  ({len(text):,} characters extracted)")
    with col_t:
        st.info(f"🔍 **{report_type}**")

    with st.expander("📄 View Extracted Text", expanded=False):
        st.text_area("Raw extracted text", text, height=220, disabled=True)

    st.divider()

    # ── Analyze button ───────────────────────────────────────
    if st.button("🤖 Analyze Report with AI", use_container_width=True, type="primary"):
        with st.spinner("🧠 Groq AI is analyzing your report — this takes about 10–20 seconds..."):
            result = analyze_medical_report(text, report_type)
        st.session_state.report_result = result
        # ── Auto-save to dashboard ──────────────────────────────────────
        if result.get("health_score", 0) > 0:
            save_report_to_dashboard(result, report_type, uploaded.name)
        st.rerun()

    # ── Results ──────────────────────────────────────────────
    ai = st.session_state.report_result
    if ai is None:
        return

    # Check if it was a fallback / error response
    if ai.get("health_score", 0) == 0 and not ai.get("possible_conditions"):
        st.error("⚠️ AI analysis failed. Please try clicking **Analyze Report** again.")
        if st.button("🔄 Retry Analysis", use_container_width=True):
            st.session_state.report_result = None
            st.rerun()
        return

    st.divider()
    st.success("✅ Analysis Completed!")

    # ── Score & Risk ─────────────────────────────────────────
    score = max(0, min(100, int(ai.get("health_score", 0))))
    risk = ai.get("risk_level", "Moderate")

    left, right = st.columns([1, 2])

    with left:
        gauge_color = "#16A34A" if score >= 70 else ("#F59E0B" if score >= 40 else "#DC2626")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Health Score", "font": {"color": "white", "size": 16}},
            number={"font": {"color": "white", "size": 40}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "white", "tickfont": {"color": "white"}},
                "bar": {"color": gauge_color},
                "bgcolor": "#172033",
                "bordercolor": "#334155",
                "steps": [
                    {"range": [0, 40],  "color": "#450a0a"},
                    {"range": [40, 70], "color": "#451a03"},
                    {"range": [70, 100],"color": "#052e16"}
                ],
                "threshold": {
                    "line": {"color": "white", "width": 2},
                    "thickness": 0.75,
                    "value": score
                }
            }
        ))
        fig.update_layout(
            height=300,
            margin=dict(t=40, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.metric("❤️ Health Score", f"{score} / 100")

        if risk == "Low":
            st.success("🟢 Risk Level: **Low** — Overall health looks good")
        elif risk == "Moderate":
            st.warning("🟡 Risk Level: **Moderate** — Some values need attention")
        else:
            st.error("🔴 Risk Level: **High** — Consult a doctor promptly")

        abnormal_count = len(ai.get("abnormal_values", []))
        if abnormal_count == 0:
            st.metric("🩸 Abnormal Values", "0", "All normal ✅")
        else:
            st.metric("🩸 Abnormal Values", abnormal_count, f"{abnormal_count} need attention ⚠️")

        st.metric("📋 Report Type", report_type)

    st.divider()

    # ── Patient Summary ──────────────────────────────────────
    st.subheader("📋 Patient Summary")
    st.markdown(
        f"""<div style="background:#172033;border-left:4px solid #2563EB;border-radius:8px;
        padding:16px 20px;color:#e2e8f0;font-size:1rem;line-height:1.7;">
        {ai.get("patient_summary","No summary available.")}
        </div>""",
        unsafe_allow_html=True
    )

    st.divider()

    # ── Abnormal Values ──────────────────────────────────────
    st.subheader("🩸 Abnormal Values")
    abnormal = ai.get("abnormal_values", [])

    if abnormal:
        rows = []
        for item in abnormal:
            if isinstance(item, dict):
                rows.append({
                    "🧪 Test":        item.get("test", ""),
                    "📊 Result":      item.get("result", ""),
                    "⚠️ Status":     item.get("status", ""),
                    "✅ Normal Range": item.get("normal_range", "")
                })
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.success("✅ All test values are within normal ranges.")

    st.divider()

    # ── Possible Conditions ──────────────────────────────────
    st.subheader("🧬 Possible Conditions")
    conditions = [c for c in ai.get("possible_conditions", []) if c and str(c).strip()]
    if conditions:
        cols = st.columns(2)
        for i, c in enumerate(conditions):
            with cols[i % 2]:
                st.info(f"🔹 {c}")
    else:
        st.success("✅ No concerning conditions identified.")

    st.divider()

    # ── Diet + Exercise ──────────────────────────────────────
    dcol, ecol = st.columns(2)

    with dcol:
        st.subheader("🥗 Diet Recommendations")
        diet = [d for d in ai.get("diet", []) if d and str(d).strip()]
        for item in diet:
            st.success(f"🥗 {item}")
        if not diet:
            st.info("No specific diet recommendations.")

    with ecol:
        st.subheader("🏃 Exercise Recommendations")
        exercise = [e for e in ai.get("exercise", []) if e and str(e).strip()]
        for item in exercise:
            st.info(f"🏃 {item}")
        if not exercise:
            st.info("No specific exercise recommendations.")

    st.divider()

    # ── Doctor Advice ────────────────────────────────────────
    st.subheader("👨‍⚕️ Doctor Advice")
    st.markdown(
        f"""<div style="background:#1c1a07;border-left:4px solid #F59E0B;border-radius:8px;
        padding:16px 20px;color:#fef3c7;font-size:1rem;line-height:1.7;">
        💬 {ai.get("doctor_advice","Please consult your healthcare provider.")}
        </div>""",
        unsafe_allow_html=True
    )

    st.divider()

    # ── Health Score Chart ───────────────────────────────────
    st.subheader("📊 Health Score Breakdown")
    remaining = 100 - score
    chart = px.pie(
        names=["Health Score", "Room for Improvement"],
        values=[score, remaining],
        color_discrete_sequence=["#2563EB", "#1e293b"],
        hole=0.65
    )
    chart.update_traces(
        textfont_size=14,
        marker=dict(line=dict(color="#0B1220", width=2))
    )
    chart.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        legend=dict(font=dict(color="white")),
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(chart, use_container_width=True)

    st.divider()

    # ── Download ─────────────────────────────────────────────
    dl_data = json.dumps(ai, indent=2, ensure_ascii=False)
    st.download_button(
        label="📥 Download Full AI Report (JSON)",
        data=dl_data,
        file_name=f"MedIntel_{report_type.replace(' ','_')}_Report.json",
        mime="application/json",
        use_container_width=True
    )
