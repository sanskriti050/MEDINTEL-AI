import streamlit as st
import os
import json
from dotenv import load_dotenv
from groq import Groq

from rag.retriever import RAGRetriever

load_dotenv()


def analyze_symptoms(age: int, gender: str, symptoms: str, duration: str, existing_conditions: str) -> dict:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # --- RAG retrieval step ---------------------------------------------
    # Retrieve the most relevant entries from our curated medical knowledge
    # base based on the patient's described symptoms, so the LLM grounds
    # its reasoning in reference data instead of relying purely on its
    # own parametric knowledge.
    retriever = RAGRetriever()
    retrieved = retriever.retrieve(symptoms, top_k=3)
    reference_context = retriever.format_context(retrieved)
    # ----------------------------------------------------------------------

    prompt = f"""You are an experienced physician with 20+ years of clinical practice.

A patient has described their symptoms. Analyze them thoroughly and provide a complete medical assessment.

Patient Profile:
- Age: {age}
- Gender: {gender}
- Symptoms: {symptoms}
- Duration: {duration}
- Existing Medical Conditions: {existing_conditions if existing_conditions else "None"}

REFERENCE MEDICAL KNOWLEDGE (retrieved from knowledge base — use this to ground your
assessment where relevant, but still use your own clinical judgment; the patient's
actual symptoms take priority over the reference if they diverge):
{reference_context}

IMPORTANT RULES:
- List ALL plausible conditions — from most to least likely. Do not limit to just 1-2.
- Be specific and detailed in your recommendations.
- Consider the patient's age, gender, and existing conditions in your analysis.
- "severity" must reflect the urgency based on the described symptoms.
- Always provide at least 3-5 items in each list field.
- Return ONLY valid JSON. No markdown, no explanation.

Return this exact JSON structure:

{{
    "possible_conditions": [
        {{
            "condition": "condition name",
            "likelihood": "High / Moderate / Low",
            "reason": "brief reason based on symptoms"
        }}
    ],
    "severity": "Mild",
    "urgency": "Can wait for appointment / See doctor within 24-48 hours / Go to ER immediately",
    "doctor_type": "type of specialist to see",
    "recommendations": [
        "specific recommendation 1",
        "specific recommendation 2"
    ],
    "home_remedies": [
        "home remedy 1",
        "home remedy 2"
    ],
    "medications_otc": [
        "OTC medicine suggestion with dosage note"
    ],
    "tests_suggested": [
        "test that doctor may recommend"
    ],
    "warning_signs": [
        "sign that means you need emergency care"
    ],
    "lifestyle_advice": [
        "lifestyle tip 1",
        "lifestyle tip 2"
    ]
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content.strip()
        if "```" in content:
            content = content.replace("```json", "").replace("```", "").strip()

        start = content.find("{")
        end = content.rfind("}") + 1
        result = json.loads(content[start:end])

        # Attach retrieved sources so the UI can show what grounded this answer
        result["_retrieved_sources"] = retrieved
        return result

    except Exception as e:
        print(f"Groq Error: {e}")
        return {
            "possible_conditions": [{"condition": "Unable to analyze", "likelihood": "N/A", "reason": "Please try again"}],
            "severity": "Unknown",
            "urgency": "Consult a doctor",
            "doctor_type": "General Physician",
            "recommendations": ["Please consult a qualified doctor"],
            "home_remedies": [],
            "medications_otc": [],
            "tests_suggested": [],
            "warning_signs": ["If symptoms worsen rapidly, seek emergency care"],
            "lifestyle_advice": []
        }


def show_symptom():
    st.title("🩺 AI Symptom Checker")
    st.caption("Describe your symptoms and get a detailed AI-powered medical assessment.")

    st.warning("⚠️ This tool is for informational purposes only and does NOT replace professional medical advice. Always consult a qualified doctor.")

    # Session state
    if "symptom_result" not in st.session_state:
        st.session_state.symptom_result = None

    with st.form("symptom_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("🔢 Age", min_value=1, max_value=120, value=25)
            duration = st.selectbox("⏱️ Duration of Symptoms", [
                "Less than 24 hours", "1-3 days", "4-7 days",
                "1-2 weeks", "More than 2 weeks", "More than a month"
            ])
        with col2:
            gender = st.selectbox("⚧ Gender", ["Male", "Female", "Other"])
            existing = st.text_input(
                "🏥 Existing Conditions (optional)",
                placeholder="e.g. Diabetes, Hypertension, Asthma..."
            )

        symptoms = st.text_area(
            "📝 Describe your symptoms in detail",
            placeholder="e.g. I have high fever (102°F), severe headache behind my eyes, body aches, nausea, and fatigue since yesterday evening. No cough or cold.",
            height=160
        )

        submitted = st.form_submit_button("🤖 Analyze Symptoms", use_container_width=True)

    if submitted:
        if not symptoms.strip():
            st.warning("Please describe your symptoms before analyzing.")
            return

        with st.spinner("🧠 AI is analyzing your symptoms..."):
            st.session_state.symptom_result = analyze_symptoms(age, gender, symptoms, duration, existing)

    result = st.session_state.symptom_result
    if result is None:
        return

    st.divider()
    st.success("✅ Analysis Complete")

    # -------------------------------------------------------
    # RAG transparency — show what reference knowledge grounded this answer
    # -------------------------------------------------------
    sources = result.get("_retrieved_sources", [])
    if sources:
        with st.expander("📚 Reference knowledge used for this assessment (RAG)"):
            for src in sources:
                st.markdown(
                    f"**{src['condition']}** — similarity: `{src['similarity_score']:.2f}`  \n"
                    f"{src['description']}"
                )

    # -------------------------------------------------------
    # Severity + Urgency
    # -------------------------------------------------------
    severity = result.get("severity", "Unknown")
    urgency = result.get("urgency", "Consult a doctor")

    scol1, scol2 = st.columns(2)
    with scol1:
        if severity == "Mild":
            st.success(f"🟢 Severity: **{severity}**")
        elif severity == "Moderate":
            st.warning(f"🟡 Severity: **{severity}**")
        else:
            st.error(f"🔴 Severity: **{severity}**")

    with scol2:
        if "ER" in urgency or "emergency" in urgency.lower():
            st.error(f"🚨 {urgency}")
        elif "24" in urgency or "48" in urgency:
            st.warning(f"⏰ {urgency}")
        else:
            st.info(f"📅 {urgency}")

    st.info(f"👨‍⚕️ Recommended Specialist: **{result.get('doctor_type', 'General Physician')}**")

    st.divider()

    # -------------------------------------------------------
    # Possible Conditions
    # -------------------------------------------------------
    st.subheader("🧬 Possible Conditions")
    conditions = result.get("possible_conditions", [])

    if conditions:
        for cond in conditions:
            if isinstance(cond, dict):
                likelihood = cond.get("likelihood", "")
                name = cond.get("condition", "")
                reason = cond.get("reason", "")

                if likelihood == "High":
                    color = "error"
                elif likelihood == "Moderate":
                    color = "warning"
                else:
                    color = "info"

                getattr(st, color)(f"**{name}** ({likelihood} likelihood) — {reason}")
            else:
                st.info(f"• {cond}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        # -------------------------------------------------------
        # Recommendations
        # -------------------------------------------------------
        st.subheader("💊 Recommendations")
        for rec in result.get("recommendations", []):
            st.success(f"✅ {rec}")

        # -------------------------------------------------------
        # OTC Medications
        # -------------------------------------------------------
        otc = result.get("medications_otc", [])
        if otc:
            st.subheader("🏪 OTC Medicines (Common)")
            for med in otc:
                st.info(f"💊 {med}")

    with col2:
        # -------------------------------------------------------
        # Home Remedies
        # -------------------------------------------------------
        st.subheader("🏠 Home Remedies")
        for remedy in result.get("home_remedies", []):
            st.info(f"🌿 {remedy}")

        # -------------------------------------------------------
        # Suggested Tests
        # -------------------------------------------------------
        tests = result.get("tests_suggested", [])
        if tests:
            st.subheader("🔬 Tests Doctor May Suggest")
            for test in tests:
                st.warning(f"🧪 {test}")

    st.divider()

    # -------------------------------------------------------
    # Lifestyle Advice
    # -------------------------------------------------------
    lifestyle = result.get("lifestyle_advice", [])
    if lifestyle:
        st.subheader("🌟 Lifestyle Advice")
        cols = st.columns(2)
        for i, tip in enumerate(lifestyle):
            with cols[i % 2]:
                st.success(f"💡 {tip}")
        st.divider()

    # -------------------------------------------------------
    # Warning Signs
    # -------------------------------------------------------
    warning_signs = result.get("warning_signs", [])
    if warning_signs:
        st.subheader("🚨 Go to Emergency If You Experience:")
        for sign in warning_signs:
            st.error(f"⚠️ {sign}")
