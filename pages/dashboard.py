import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, date
import json

# ── Session state initializer ─────────────────────────────────────────────────
def _init_state():
    if "dash_reports" not in st.session_state:
        st.session_state.dash_reports = []          # list of report dicts
    if "dash_metrics" not in st.session_state:
        st.session_state.dash_metrics = []          # list of metric dicts
    if "dash_profile" not in st.session_state:
        st.session_state.dash_profile = {
            "name": "", "age": 25, "gender": "Male",
            "weight": 70.0, "height": 170.0, "blood_group": "A+"
        }


# ── Derived helpers ───────────────────────────────────────────────────────────
def _avg_score(reports):
    if not reports:
        return 0
    return round(sum(r["score"] for r in reports) / len(reports), 1)

def _risk_color(risk):
    return {"Low": "#16A34A", "Moderate": "#c38a3e", "High": "#b94c46"}.get(risk, "#bdb590")

def _score_color(score):
    if score >= 70: return "#16A34A"
    if score >= 40: return "#c38a3e"
    return "#b94c46"

def _bmi(w, h):
    if h <= 0: return 0
    return round(w / (h / 100) ** 2, 1)

def _bmi_label(bmi):
    if bmi < 18.5: return "Underweight", "#b8a070"
    if bmi < 25:   return "Normal",      "#9aa678"
    if bmi < 30:   return "Overweight",  "#c38a3e"
    return "Obese", "#b94c46"


# ── Gauge chart ───────────────────────────────────────────────────────────────
def _gauge(value, title, height=260):
    color = _score_color(value)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"color": "#1f3f2d", "size": 14}},
        number={"font": {"color": "#1f3f2d", "size": 36}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#22513a",
                     "tickfont": {"color": "#22513a", "size": 10}},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "#e8f6e8", "bordercolor": "#c7e1c7",
            "steps": [
                {"range": [0, 40],   "color": "#d7eddb"},
                {"range": [40, 70],  "color": "#bde4c0"},
                {"range": [70, 100], "color": "#94d29a"},
            ],
            "threshold": {"line": {"color": color, "width": 3},
                          "thickness": 0.75, "value": value}
        }
    ))
    fig.update_layout(height=height, margin=dict(t=40, b=0, l=10, r=10),
                      paper_bgcolor="rgba(0,0,0,0)")
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# MAIN FUNCTION
# ─────────────────────────────────────────────────────────────────────────────
def show_dashboard():
    _init_state()

    st.title("📊 Health Dashboard")
    st.caption("Your personal health command center — add reports, track vitals, and monitor trends.")

    # ── TABS ─────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Overview", "➕ Add Report", "🩺 Health Vitals", "⚙️ My Profile"
    ])

    # ════════════════════════════════════════════════════════════════════════
    # TAB 1 — OVERVIEW
    # ════════════════════════════════════════════════════════════════════════
    with tab1:
        reports = st.session_state.dash_reports
        profile = st.session_state.dash_profile

        if not reports:
            st.markdown("""
            <div style="background:#f3fbf5;border:1px dashed rgba(105, 179, 114, 0.28);border-radius:16px;
            padding:48px;text-align:center;">
                <div style="font-size:3rem;">📋</div>
                <h3 style="color:#214d39;margin:12px 0 8px 0;">No reports yet</h3>
                <p style="color:#3f6451;font-size:1rem;">
                    Analyze a report on the <b>📄 Report Analyzer</b> page —
                    it will appear here automatically.<br>
                    Or go to <b>➕ Add Report</b> tab to log one manually.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            avg  = _avg_score(reports)
            last = reports[-1]
            risks = {"Low": 0, "Moderate": 0, "High": 0}
            for r in reports:
                risks[r["risk"]] = risks.get(r["risk"], 0) + 1

            # ── Summary cards ────────────────────────────────────────────────
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("📄 Total Reports", len(reports), f"+{min(len(reports),1)} added")
            c2.metric("❤️ Avg Health Score", f"{avg}/100",
                      f"{'+' if avg >= 70 else ''}{round(avg-70,1)} vs target")
            c3.metric("🏆 Latest Score", f"{last['score']}/100",
                      f"{'↑' if len(reports)<2 else ('↑' if last['score']>=reports[-2]['score'] else '↓')}")
            c4.metric("⚠️ Latest Risk", last["risk"],
                      "🟢" if last["risk"]=="Low" else ("🟡" if last["risk"]=="Moderate" else "🔴"))

            st.divider()

            # ── Score trend chart ────────────────────────────────────────────
            st.subheader("📈 Health Score Trend")
            df_trend = pd.DataFrame(reports)
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=df_trend["date"], y=df_trend["score"],
                mode="lines+markers+text",
                text=df_trend["score"],
                textposition="top center",
                textfont=dict(color="#1f3f2d", size=11),
                line=dict(color="#3f8d66", width=3),
                marker=dict(size=10, color=df_trend["score"].apply(_score_color),
                            line=dict(color="#ffffff", width=2)),
                fill="tozeroy",
                fillcolor="rgba(83, 185, 137, 0.12)",
                hovertemplate="<b>%{x}</b><br>Score: %{y}/100<br>Type: " +
                              df_trend["report_type"].astype(str) + "<extra></extra>"
            ))
            # target line at 70
            fig_trend.add_hline(y=70, line_dash="dash", line_color="#9aa678",
                                annotation_text="Target (70)", annotation_font_color="#9aa678")
            fig_trend.update_layout(
                height=320, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(range=[0, 105], gridcolor="#cfe8d0", tickfont=dict(color="#22513a")),
                xaxis=dict(gridcolor="#cfe8d0", tickfont=dict(color="#22513a"), tickangle=-30),
                font=dict(color="#1f3f2d"), margin=dict(t=20, b=40),
                showlegend=False
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            st.divider()

            # ── Gauge + Risk pie ──────────────────────────────────────────────
            g1, g2 = st.columns(2)
            with g1:
                st.subheader("❤️ Latest Health Score")
                st.plotly_chart(_gauge(last["score"], "Health Score"), use_container_width=True)
            with g2:
                st.subheader("🧬 Risk Distribution")
                risk_vals = [risks.get(k, 0) for k in ["Low", "Moderate", "High"]]
                if sum(risk_vals) > 0:
                    fig_pie = px.pie(
                        names=["Low Risk", "Moderate Risk", "High Risk"],
                        values=risk_vals,
                        color_discrete_sequence=["#7ca16d", "#c3a36f", "#c65a57"],
                        hole=0.55
                    )
                    fig_pie.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)",
                                          font=dict(color="#1f3f2d"),
                                          legend=dict(font=dict(color="#1f3f2d")),
                                          margin=dict(t=20,b=20))
                    st.plotly_chart(fig_pie, use_container_width=True)
            st.divider()

            # ── Report type bar chart ─────────────────────────────────────────
            st.subheader("📊 Reports by Type")
            type_counts = df_trend["report_type"].value_counts().reset_index()
            type_counts.columns = ["Report Type", "Count"]
            fig_bar = px.bar(type_counts, x="Report Type", y="Count",
                             color="Count",
                             color_continuous_scale=["#314d39", "#7c9e74", "#b49773"],
                             text="Count")
            fig_bar.update_traces(textposition="outside", textfont_color="#1f3f2d")
            fig_bar.update_layout(
                height=280, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(tickfont=dict(color="#22513a"), gridcolor="#cfe8d0"),
                yaxis=dict(tickfont=dict(color="#22513a"), gridcolor="#cfe8d0"),
                font=dict(color="#1f3f2d"), margin=dict(t=20,b=40),
                coloraxis_showscale=False, showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            st.divider()

            # ── Full report history table ─────────────────────────────────────
            st.subheader("📋 Report History")
            display_df = df_trend[["date","report_type","score","risk","abnormal_count","notes"]].copy()
            # Add source column if exists
            if "source" in df_trend.columns:
                display_df["source"] = df_trend["source"].map(
                    {"auto": "🤖 Auto", "manual": "✍️ Manual"}).fillna("✍️ Manual")
                display_df = display_df[["date","report_type","score","risk","abnormal_count","source","notes"]]
                display_df.columns = ["📅 Date","📄 Report Type","💯 Score","⚠️ Risk",
                                       "🩸 Abnormal","📥 Source","📝 Notes"]
            else:
                display_df.columns = ["📅 Date","📄 Report Type","💯 Score","⚠️ Risk",
                                       "🩸 Abnormal Values","📝 Notes"]
            display_df["⚠️ Risk"] = display_df["⚠️ Risk"].map(
                {"Low":"🟢 Low", "Moderate":"🟡 Moderate", "High":"🔴 High"})
            st.dataframe(display_df, use_container_width=True, hide_index=True)

            # Delete last report
            if st.button("🗑️ Delete Last Report", type="secondary"):
                st.session_state.dash_reports.pop()
                st.rerun()


    # ════════════════════════════════════════════════════════════════════════
    # TAB 2 — ADD REPORT
    # ════════════════════════════════════════════════════════════════════════
    with tab2:
        st.subheader("➕ Log a Health Report")
        st.info("Fill in the details from your medical report to track it on the dashboard.")

        with st.form("add_report_form", clear_on_submit=True):
            r1, r2 = st.columns(2)
            with r1:
                rep_date = st.date_input("📅 Report Date", value=date.today())
                rep_type = st.selectbox("📄 Report Type", [
                    "Blood / CBC Report", "Lipid / Cholesterol Report",
                    "Thyroid Profile", "Liver Function Test", "Kidney Function Test",
                    "Diabetes / Blood Sugar Report", "Vitamin & Mineral Profile",
                    "Urine Analysis Report", "Cardiac Report",
                    "Radiology / Imaging Report", "Hormone Profile",
                    "Infection / Immunity Report", "General Medical Report"
                ])
                health_score = st.slider("💯 Health Score (from AI analysis)", 0, 100, 75)
            with r2:
                risk_level = st.selectbox("⚠️ Risk Level", ["Low", "Moderate", "High"])
                abnormal_count = st.number_input("🩸 No. of Abnormal Values", 0, 50, 0)
                notes = st.text_input("📝 Notes (optional)",
                                      placeholder="e.g. Hemoglobin low, follow-up needed")

            st.markdown("**🔬 Key Test Values (optional — for vitals tracking)**")
            v1, v2, v3 = st.columns(3)
            with v1:
                hemoglobin = st.text_input("Hemoglobin (g/dL)", placeholder="e.g. 13.5")
                cholesterol = st.text_input("Total Cholesterol (mg/dL)", placeholder="e.g. 185")
            with v2:
                blood_sugar = st.text_input("Blood Sugar / Glucose (mg/dL)", placeholder="e.g. 95")
                tsh = st.text_input("TSH (mIU/L)", placeholder="e.g. 2.5")
            with v3:
                creatinine = st.text_input("Creatinine (mg/dL)", placeholder="e.g. 0.9")
                vitamin_d = st.text_input("Vitamin D (ng/mL)", placeholder="e.g. 28")

            submitted = st.form_submit_button("✅ Save Report", use_container_width=True)

        if submitted:
            def _safe_float(val):
                try: return float(val.strip()) if val.strip() else None
                except: return None

            entry = {
                "date":          str(rep_date),
                "report_type":   rep_type,
                "score":         health_score,
                "risk":          risk_level,
                "abnormal_count":abnormal_count,
                "notes":         notes or "—",
                "source":        "manual",
                "filename":      "manual-entry",
                "hemoglobin":    _safe_float(hemoglobin),
                "cholesterol":   _safe_float(cholesterol),
                "blood_sugar":   _safe_float(blood_sugar),
                "tsh":           _safe_float(tsh),
                "creatinine":    _safe_float(creatinine),
                "vitamin_d":     _safe_float(vitamin_d),
                "added_at":      datetime.now().isoformat()
            }
            st.session_state.dash_reports.append(entry)
            st.success(f"✅ Report saved! Health Score: **{health_score}/100** | Risk: **{risk_level}**")
            st.balloons()


    # ════════════════════════════════════════════════════════════════════════
    # TAB 3 — HEALTH VITALS
    # ════════════════════════════════════════════════════════════════════════
    with tab3:
        st.subheader("🩺 Health Vitals Tracker")

        reports = st.session_state.dash_reports
        if not reports:
            st.info("Add reports from the **➕ Add Report** tab to see vitals charts.")
        else:
            df_v = pd.DataFrame(reports)

            # Define vitals to chart
            vitals_cfg = [
                ("hemoglobin",  "Hemoglobin",        "g/dL",   11.0, 17.0, "#a57c53"),
                ("cholesterol", "Total Cholesterol",  "mg/dL",  0,    200,  "#c38a3e"),
                ("blood_sugar", "Blood Sugar",        "mg/dL",  70,   100,  "#9aa678"),
                ("tsh",         "TSH",                "mIU/L",  0.4,  4.0,  "#b5945a"),
                ("creatinine",  "Creatinine",         "mg/dL",  0.7,  1.2,  "#b94c46"),
                ("vitamin_d",   "Vitamin D",          "ng/mL",  20,   50,   "#d8b56f"),
            ]

            # Only show vitals that have at least 1 non-null entry
            available = [(k,lbl,unit,lo,hi,col)
                         for k,lbl,unit,lo,hi,col in vitals_cfg
                         if k in df_v.columns and df_v[k].notna().any()]

            if not available:
                st.info("No vital values found. When adding a report, fill in the key test values to see charts here.")
            else:
                # Pair into rows of 2
                for i in range(0, len(available), 2):
                    cols_pair = st.columns(2)
                    for j, cfg in enumerate(available[i:i+2]):
                        key, label, unit, lo, hi, color = cfg
                        with cols_pair[j]:
                            data = df_v[["date", key]].dropna()
                            if data.empty:
                                continue
                            latest_val = data[key].iloc[-1]
                            status = "✅ Normal" if lo <= latest_val <= hi else \
                                     ("⬆️ High" if latest_val > hi else "⬇️ Low")
                            st.markdown(
                                f"""<div style="background:#f7fdf4;border:1px solid #d7ebd6;
                                border-left:4px solid {color};border-radius:12px;
                                padding:12px 16px;margin-bottom:4px;display:flex;
                                justify-content:space-between;align-items:center;">
                                <div><b style="color:#1e4331;font-size:1rem;">{label}</b>
                                <p style="color:#4e7f60;font-size:0.78rem;margin:2px 0 0 0;">
                                Normal: {lo}–{hi} {unit}</p></div>
                                <div style="text-align:right;">
                                <b style="color:{color};font-size:1.4rem;">{latest_val} {unit}</b>
                                <p style="color:#4e7f60;font-size:0.8rem;margin:2px 0 0 0;">{status}</p>
                                </div></div>""",
                                unsafe_allow_html=True
                            )
                            if len(data) > 1:
                                fig_v = go.Figure()
                                fig_v.add_trace(go.Scatter(
                                    x=data["date"], y=data[key],
                                    mode="lines+markers",
                                    line=dict(color=color, width=2),
                                    marker=dict(size=7, color=color),
                                    fill="tozeroy", fillcolor=f"rgba(165,124,83,0.08)"
                                ))
                                fig_v.add_hrect(y0=lo, y1=hi,
                                               fillcolor="rgba(74,222,128,0.07)",
                                               line_width=0,
                                               annotation_text="Normal range",
                                               annotation_font_color="#4ADE80",
                                               annotation_position="top right")
                                fig_v.update_layout(
                                    height=180, margin=dict(t=10,b=30,l=10,r=10),
                                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                    xaxis=dict(tickfont=dict(color="#22513a", size=9), gridcolor="#d3ecdb"),
                                    yaxis=dict(tickfont=dict(color="#22513a", size=9), gridcolor="#d3ecdb"),
                                    showlegend=False
                                )
                                st.plotly_chart(fig_v, use_container_width=True)
                    st.markdown("")

        # ── Manual vitals entry ───────────────────────────────────────────
        st.divider()
        st.subheader("➕ Log Today's Vitals Manually")
        with st.form("vitals_form", clear_on_submit=True):
            mv1, mv2, mv3, mv4 = st.columns(4)
            with mv1:
                bp_sys = st.number_input("🩺 BP Systolic", 80, 200, 120)
                bp_dia = st.number_input("🩺 BP Diastolic", 50, 130, 80)
            with mv2:
                heart_rate = st.number_input("💓 Heart Rate (bpm)", 40, 200, 72)
                spo2 = st.number_input("🫁 SpO2 (%)", 80, 100, 98)
            with mv3:
                temp = st.number_input("🌡️ Temp (°F)", 95.0, 106.0, 98.6, step=0.1)
                weight_today = st.number_input("⚖️ Weight (kg)", 30.0, 200.0,
                    float(st.session_state.dash_profile.get("weight", 70)), step=0.5)
            with mv4:
                water = st.number_input("💧 Water intake (glasses)", 0, 20, 8)
                sleep_hrs = st.number_input("😴 Sleep (hrs)", 0.0, 12.0, 7.0, step=0.5)

            v_submit = st.form_submit_button("💾 Save Today's Vitals", use_container_width=True)

        if v_submit:
            entry = {
                "date": str(date.today()),
                "bp": f"{bp_sys}/{bp_dia}",
                "heart_rate": heart_rate,
                "spo2": spo2,
                "temp": temp,
                "weight": weight_today,
                "water": water,
                "sleep": sleep_hrs
            }
            if "dash_daily_vitals" not in st.session_state:
                st.session_state.dash_daily_vitals = []
            st.session_state.dash_daily_vitals.append(entry)

            # Quick feedback
            alerts = []
            if bp_sys > 140:       alerts.append("⚠️ High systolic BP")
            if heart_rate > 100:   alerts.append("⚠️ Heart rate elevated")
            if spo2 < 95:          alerts.append("🚨 Low SpO2 — consult doctor")
            if temp > 99.5:        alerts.append("⚠️ Mild fever detected")
            if water < 6:          alerts.append("💧 Drink more water today")
            if sleep_hrs < 6:      alerts.append("😴 Poor sleep — rest more")

            st.success("✅ Vitals saved!")
            for a in alerts:
                st.warning(a)

        # Show daily vitals history
        if "dash_daily_vitals" in st.session_state and st.session_state.dash_daily_vitals:
            st.divider()
            st.subheader("📅 Daily Vitals Log")
            dv_df = pd.DataFrame(st.session_state.dash_daily_vitals)
            dv_df.columns = ["📅 Date","🩺 BP","💓 HR (bpm)","🫁 SpO2 %",
                              "🌡️ Temp °F","⚖️ Wt (kg)","💧 Water","😴 Sleep (h)"]
            st.dataframe(dv_df, use_container_width=True, hide_index=True)

            # Weight trend if multiple entries
            if len(st.session_state.dash_daily_vitals) > 1:
                wt_df = pd.DataFrame(st.session_state.dash_daily_vitals)[["date","weight"]]
                fig_wt = px.line(wt_df, x="date", y="weight",
                                 title="⚖️ Weight Trend",
                                 markers=True,
                                 color_discrete_sequence=["#FBBF24"])
                fig_wt.update_layout(
                    height=220, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#1f3f2d"), margin=dict(t=40,b=30,l=10,r=10),
                    xaxis=dict(gridcolor="#d3ecdb", tickfont=dict(color="#22513a")),
                    yaxis=dict(gridcolor="#d3ecdb", tickfont=dict(color="#22513a")),
                    title_font_color="#1f3f2d"
                )
                st.plotly_chart(fig_wt, use_container_width=True)


    # ════════════════════════════════════════════════════════════════════════
    # TAB 4 — MY PROFILE
    # ════════════════════════════════════════════════════════════════════════
    with tab4:
        st.subheader("⚙️ My Health Profile")
        profile = st.session_state.dash_profile

        with st.form("profile_form"):
            p1, p2 = st.columns(2)
            with p1:
                name   = st.text_input("👤 Full Name", value=profile.get("name",""))
                age    = st.number_input("🔢 Age", 1, 120, int(profile.get("age", 25)))
                gender = st.selectbox("⚧ Gender", ["Male","Female","Other"],
                                      index=["Male","Female","Other"].index(
                                          profile.get("gender","Male")))
                blood  = st.selectbox("🩸 Blood Group",
                                      ["A+","A-","B+","B-","AB+","AB-","O+","O-","Unknown"],
                                      index=["A+","A-","B+","B-","AB+","AB-","O+","O-","Unknown"]
                                      .index(profile.get("blood_group","A+")))
            with p2:
                weight = st.number_input("⚖️ Weight (kg)", 10.0, 300.0,
                                         float(profile.get("weight",70.0)), step=0.5)
                height = st.number_input("📏 Height (cm)", 50.0, 250.0,
                                         float(profile.get("height",170.0)), step=0.5)
                conditions = st.text_input("🏥 Existing Conditions",
                                           value=profile.get("conditions",""),
                                           placeholder="e.g. Diabetes, Hypertension")
                allergies  = st.text_input("🚫 Allergies",
                                           value=profile.get("allergies",""),
                                           placeholder="e.g. Penicillin, Dust")

            p_save = st.form_submit_button("💾 Save Profile", use_container_width=True)

        if p_save:
            st.session_state.dash_profile = {
                "name": name, "age": age, "gender": gender,
                "blood_group": blood, "weight": weight, "height": height,
                "conditions": conditions, "allergies": allergies
            }
            st.success("✅ Profile saved!")
            profile = st.session_state.dash_profile

        # Display profile card + BMI
        p = st.session_state.dash_profile
        if p.get("name"):
            st.divider()
            bmi_val   = _bmi(p.get("weight",70), p.get("height",170))
            bmi_lab, bmi_col = _bmi_label(bmi_val)

            st.markdown(f"""
            <div style="background:#f4fbea;border:1px solid #d0e9cf;border-radius:16px;
            padding:24px 28px;">
                <h3 style="color:#1d4734;margin:0 0 16px 0;">👤 {p.get('name','—')}</h3>
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;
                flex-wrap:wrap;">
                    <div><p style="color:#5c7660;margin:0;font-size:0.8rem;">AGE</p>
                    <b style="color:#1f4736;">{p.get('age','—')} yrs</b></div>
                    <div><p style="color:#5c7660;margin:0;font-size:0.8rem;">GENDER</p>
                    <b style="color:#1f4736;">{p.get('gender','—')}</b></div>
                    <div><p style="color:#5c7660;margin:0;font-size:0.8rem;">BLOOD GROUP</p>
                    <b style="color:#d33b4e;">{p.get('blood_group','—')}</b></div>
                    <div><p style="color:#5c7660;margin:0;font-size:0.8rem;">WEIGHT / HEIGHT</p>
                    <b style="color:#1f4736;">{p.get('weight','—')} kg / {p.get('height','—')} cm</b></div>
                    <div><p style="color:#5c7660;margin:0;font-size:0.8rem;">BMI</p>
                    <b style="color:{bmi_col};">{bmi_val} — {bmi_lab}</b></div>
                    <div><p style="color:#5c7660;margin:0;font-size:0.8rem;">CONDITIONS</p>
                    <b style="color:#b58820;">{p.get('conditions','None') or 'None'}</b></div>
                    <div><p style="color:#5c7660;margin:0;font-size:0.8rem;">ALLERGIES</p>
                    <b style="color:#d33b4e;">{p.get('allergies','None') or 'None'}</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # BMI gauge
            st.markdown("<br>", unsafe_allow_html=True)
            c_bmi1, c_bmi2 = st.columns([1,2])
            with c_bmi1:
                fig_bmi = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=bmi_val,
                    title={"text":"BMI","font":{"color":"#1f3f2d"}},
                    number={"font":{"color":"#1f3f2d"}},
                    gauge={
                        "axis":{"range":[10,45],"tickcolor":"#22513a",
                                "tickfont":{"color":"#22513a"}},
                        "bar":{"color":bmi_col},
                        "bgcolor":"#eefaf0","bordercolor":"#d2e7d4",
                        "steps":[
                            {"range":[10,18.5],"color":"#eaf7ec"},
                            {"range":[18.5,25],"color":"#d7edd8"},
                            {"range":[25,30],  "color":"#bde4c0"},
                            {"range":[30,45],  "color":"#9ad89a"},
                        ]
                    }
                ))
                fig_bmi.update_layout(height=250, paper_bgcolor="rgba(0,0,0,0)",
                                      margin=dict(t=40,b=0,l=10,r=10))
                st.plotly_chart(fig_bmi, use_container_width=True)

            with c_bmi2:
                st.markdown("""
                <div style="margin-top:20px;">
                <p style="color:#c8bfa1;font-size:0.9rem;line-height:2;">
                <span style="color:#b8a070;">■</span> &lt;18.5 — Underweight<br>
                <span style="color:#9aa678;">■</span> 18.5–24.9 — Normal weight<br>
                <span style="color:#c38a3e;">■</span> 25–29.9 — Overweight<br>
                <span style="color:#b94c46;">■</span> ≥30 — Obese
                </p></div>
                """, unsafe_allow_html=True)
