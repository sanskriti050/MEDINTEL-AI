import streamlit as st
import os
import json
from html import escape
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def get_medicine_info(medicine_name: str) -> dict:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""You are a senior clinical pharmacist with deep knowledge of all medicines worldwide.

The user wants information about: "{medicine_name}"

This could be:
- Any Indian brand name (Dolo, Crocin, Combiflam, Augmentin, Metrogyl, Pantop, Shelcal, Ecosprin, Revital, etc.)
- Any international brand name (Tylenol, Advil, Xanax, Lipitor, Nexium, etc.)
- Any generic/salt name (Paracetamol, Ibuprofen, Amoxicillin, Metformin, Pantoprazole, etc.)
- Any supplement, vitamin, OTC drug, prescription drug, antibiotic, antifungal, etc.

YOUR JOB: Provide COMPLETE, ACCURATE, DETAILED pharmaceutical information about this medicine.

MANDATORY RULES:
- You MUST provide information. Never say "I cannot provide", "I don't know", or leave fields empty.
- If you recognize the brand name, use its exact generic/salt name.
- If it is a combination drug, mention all active ingredients.
- All fields are REQUIRED. Never use null.
- Return ONLY a valid JSON object. No markdown. No explanation. No text outside JSON.

Return EXACTLY this JSON:

{{
  "name": "{medicine_name}",
  "generic_name": "active ingredient(s) / salt name",
  "manufacturer": "manufacturer or N/A",
  "drug_class": "pharmacological class",
  "mechanism": "how this drug works in the body in 2-3 sentences",
  "uses": [
    "Primary use 1",
    "Primary use 2",
    "Use 3",
    "Use 4",
    "Use 5"
  ],
  "dosage": {{
    "adult": "adult dose with strength e.g. 500mg twice daily",
    "child": "child dose or Not recommended under X years",
    "frequency": "how many times per day",
    "duration": "typical course duration",
    "max_dose": "maximum safe dose per day"
  }},
  "side_effects": {{
    "common": ["side effect 1", "side effect 2", "side effect 3", "side effect 4"],
    "serious": ["serious effect 1", "serious effect 2"],
    "rare": ["rare effect 1", "rare effect 2"]
  }},
  "contraindications": [
    "Who should NOT take this medicine — condition 1",
    "Who should NOT take this medicine — condition 2",
    "Who should NOT take this medicine — condition 3"
  ],
  "interactions": [
    "Drug/food interaction 1 with brief explanation",
    "Drug/food interaction 2 with brief explanation",
    "Drug/food interaction 3 with brief explanation"
  ],
  "precautions": [
    "Precaution 1",
    "Precaution 2",
    "Precaution 3",
    "Precaution 4"
  ],
  "storage": "Storage instructions including temperature",
  "pregnancy_category": "Safe / Avoid / Category B / Category C / Consult doctor with brief reason",
  "breastfeeding": "Safe / Not safe / Consult doctor with brief reason",
  "otc_or_prescription": "OTC / Prescription / Schedule H / Schedule H1 / Schedule X",
  "overdose": "Symptoms of overdose and what to do immediately",
  "missed_dose": "What to do if a dose is missed",
  "alcohol": "Safe to use with alcohol / Avoid alcohol / Consult doctor — brief reason"
}}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=2500,
            messages=[
                {
                    "role": "system",
                    "content": "You are a clinical pharmacist AI. You ONLY output valid JSON with complete pharmaceutical data. You never refuse or give incomplete information. You know all medicines including Indian brands."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()

        start = content.find("{")
        end = content.rfind("}") + 1
        if start == -1:
            raise ValueError("No JSON in response")

        result = json.loads(content[start:end])

        # Ensure all required keys exist with defaults
        result.setdefault("name", medicine_name)
        result.setdefault("generic_name", "N/A")
        result.setdefault("manufacturer", "N/A")
        result.setdefault("drug_class", "N/A")
        result.setdefault("mechanism", "Information not available.")
        result.setdefault("uses", [])
        result.setdefault("dosage", {})
        result.setdefault("side_effects", {"common": [], "serious": [], "rare": []})
        result.setdefault("contraindications", [])
        result.setdefault("interactions", [])
        result.setdefault("precautions", [])
        result.setdefault("storage", "Store at room temperature away from moisture and direct sunlight.")
        result.setdefault("pregnancy_category", "Consult doctor")
        result.setdefault("breastfeeding", "Consult doctor")
        result.setdefault("otc_or_prescription", "Consult pharmacist")
        result.setdefault("overdose", "Seek immediate medical attention or call poison control.")
        result.setdefault("missed_dose", "Take as soon as remembered. Skip if next dose is near.")
        result.setdefault("alcohol", "Consult doctor")

        return result

    except Exception as e:
        print(f"Groq Error: {e}")
        return {
            "name": medicine_name,
            "generic_name": "Error fetching data",
            "manufacturer": "N/A",
            "drug_class": "N/A",
            "mechanism": "Could not fetch information. Please check your internet connection and try again.",
            "uses": ["Please try searching again"],
            "dosage": {"adult": "N/A", "child": "N/A", "frequency": "N/A", "duration": "N/A", "max_dose": "N/A"},
            "side_effects": {"common": [], "serious": [], "rare": []},
            "contraindications": [],
            "interactions": [],
            "precautions": ["Always consult a doctor or pharmacist"],
            "storage": "Store as directed",
            "pregnancy_category": "Consult doctor",
            "breastfeeding": "Consult doctor",
            "otc_or_prescription": "Unknown",
            "overdose": "Seek immediate medical attention",
            "missed_dose": "Take as soon as remembered",
            "alcohol": "Consult doctor"
        }


def show_medicine():
    st.title("💊 Medicine Guide")
    st.caption("Search any medicine — Indian brands, generic names, salts, supplements, antibiotics, and more.")

    st.warning("⚠️ For informational purposes only. Always follow your doctor's prescription.")

    if "medicine_result" not in st.session_state:
        st.session_state.medicine_result = None
    if "medicine_query" not in st.session_state:
        st.session_state.medicine_query = ""

    medicine = st.text_input(
        "🔍 Enter Medicine Name",
        placeholder="e.g. Dolo 650, Crocin, Paracetamol, Azithromycin, Pantoprazole, Metformin, Shelcal, Revital...",
    )

    if st.button("🔎 Get Medicine Info", use_container_width=True, type="primary"):
        if not medicine.strip():
            st.warning("Please enter a medicine name first.")
            return
        if medicine.strip() != st.session_state.medicine_query:
            st.session_state.medicine_result = None
        st.session_state.medicine_query = medicine.strip()
        with st.spinner(f"🔬 Fetching complete information for **{medicine}**..."):
            st.session_state.medicine_result = get_medicine_info(medicine.strip())

    info = st.session_state.medicine_result
    if info is None:
        st.markdown("""
        **Try searching for:**
        - 💊 Indian brands: `Dolo 650`, `Crocin`, `Combiflam`, `Augmentin`, `Metrogyl`, `Pantop`, `Shelcal`
        - 💉 Generic names: `Paracetamol`, `Ibuprofen`, `Amoxicillin`, `Metformin`, `Atorvastatin`
        - 🌿 Supplements: `Vitamin D3`, `Vitamin B12`, `Zinc`, `Calcium`, `Omega 3`
        - 🧪 Antibiotics: `Azithromycin`, `Ciprofloxacin`, `Amoxiclav`, `Cefixime`
        """)
        return

    st.divider()

    # ── Header ─────────────────────────────────────────────────
    st.markdown(
        f"""<div style="background:#B2B7BB;border:1px solid #4CA9EE;border-radius:14px;padding:20px 24px;margin-bottom:16px;">
        <h2 style="color:white;margin:0 0 4px 0;">💊 {info.get('name', medicine)}</h2>
        <p style="color:#238878;margin:0;">
            <b style="color:#4CA9EE;">Generic:</b> {info.get('generic_name','N/A')} &nbsp;|&nbsp;
            <b style="color:#4CA9EE;">Manufacturer:</b> {info.get('manufacturer','N/A')}
        </p>
        </div>""",
        unsafe_allow_html=True
    )

    # ── Top medicine details ────────────────────────────────────
    # Custom cards are used here instead of st.metric because Streamlit
    # truncates long values with an ellipsis on narrow columns.
    st.markdown("""
        <style>
        .medicine-detail-card {
            background: #B2B7BB;
            border: 1px solid #238878;
            border-radius: 15px;
            box-sizing: border-box;
            min-height: 126px;
            padding: 18px;
        }
        .medicine-detail-label {
            color: #238878 !important;
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .medicine-detail-value {
            color: #238878 !important;
            font-size: clamp(0.95rem, 1.6vw, 1.35rem);
            font-weight: 400;
            line-height: 1.25;
            overflow-wrap: anywhere;
            word-break: break-word;
            white-space: normal;
        }
        </style>
    """, unsafe_allow_html=True)

    def detail_card(column, label, value):
        safe_label = escape(str(label))
        safe_value = escape(str(value or "N/A"))
        column.markdown(
            f"""<div class="medicine-detail-card">
                <div class="medicine-detail-label">{safe_label}</div>
                <div class="medicine-detail-value">{safe_value}</div>
            </div>""",
            unsafe_allow_html=True,
        )

    c1, c2, c3, c4 = st.columns(4)
    detail_card(c1, "🏷️ Drug Class", info.get("drug_class", "N/A"))
    detail_card(c2, "📋 Schedule", info.get("otc_or_prescription", "N/A"))
    detail_card(c3, "🤰 Pregnancy", info.get("pregnancy_category", "N/A"))
    detail_card(c4, "🍼 Breastfeeding", info.get("breastfeeding", "N/A"))

    st.divider()

    # ── Mechanism ───────────────────────────────────────────────
    mechanism = info.get("mechanism", "")
    if mechanism and mechanism not in ("N/A", "Information not available."):
        st.subheader("⚙️ How It Works")
        st.markdown(
            f"""<div style="background:#4CA9EE;border-left:4px solid #4CA9EE;border-radius:8px;
            padding:14px 18px;color:#4CA9EE;line-height:1.7;">{mechanism}</div>""",
            unsafe_allow_html=True
        )
        st.divider()

    # ── Uses ────────────────────────────────────────────────────
    st.subheader("✅ Uses & Indications")
    uses = info.get("uses", [])
    if uses:
        cols = st.columns(2)
        for i, use in enumerate(uses):
            with cols[i % 2]:
                st.success(f"• {use}")
    else:
        st.info("No uses listed.")

    st.divider()

    # ── Dosage ──────────────────────────────────────────────────
    st.subheader("📏 Dosage Guide")
    dosage = info.get("dosage", {})
    if isinstance(dosage, dict) and dosage:
        d1, d2 = st.columns(2)
        with d1:
            st.info(f"👨 **Adult Dose:** {dosage.get('adult', 'N/A')}")
            st.info(f"🔁 **Frequency:** {dosage.get('frequency', 'N/A')}")
            st.info(f"⏱️ **Duration:** {dosage.get('duration', 'N/A')}")
        with d2:
            st.info(f"👶 **Child Dose:** {dosage.get('child', 'N/A')}")
            st.info(f"🚨 **Max Daily Dose:** {dosage.get('max_dose', 'N/A')}")
    else:
        st.info("Consult your doctor for dosage.")

    st.divider()

    # ── Side Effects ────────────────────────────────────────────
    st.subheader("⚠️ Side Effects")
    se = info.get("side_effects", {})
    if isinstance(se, dict):
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown("**🟡 Common**")
            for e in se.get("common", []):
                st.warning(f"• {e}")
            if not se.get("common"):
                st.caption("None listed")
        with s2:
            st.markdown("**🔴 Serious**")
            for e in se.get("serious", []):
                st.error(f"• {e}")
            if not se.get("serious"):
                st.caption("None listed")
        with s3:
            st.markdown("**🔵 Rare**")
            for e in se.get("rare", []):
                st.info(f"• {e}")
            if not se.get("rare"):
                st.caption("None listed")
    elif isinstance(se, list):
        for e in se:
            st.warning(f"• {e}")

    st.divider()

    # ── Contraindications + Interactions ────────────────────────
    ca, cb = st.columns(2)

    with ca:
        st.subheader("🚫 Contraindications")
        contras = info.get("contraindications", [])
        if contras:
            for c in contras:
                st.error(f"❌ {c}")
        else:
            st.success("No major contraindications listed.")

    with cb:
        st.subheader("⚡ Drug & Food Interactions")
        interactions = info.get("interactions", [])
        if interactions:
            for inter in interactions:
                st.warning(f"⚠️ {inter}")
        else:
            st.success("No major interactions listed.")

    st.divider()

    # ── Precautions + Storage ────────────────────────────────────
    pa, pb = st.columns(2)

    with pa:
        st.subheader("🛡️ Precautions")
        for p in info.get("precautions", []):
            st.info(f"🔹 {p}")

    with pb:
        st.subheader("📦 Storage Instructions")
        st.info(f"🌡️ {info.get('storage', 'Store as directed')}")

    st.divider()

    # ── Overdose / Missed / Alcohol ──────────────────────────────
    oc, od, oe = st.columns(3)

    with oc:
        st.subheader("🚨 Overdose")
        st.error(f"⚠️ {info.get('overdose', 'Seek immediate medical attention')}")

    with od:
        st.subheader("⏰ Missed Dose")
        st.warning(f"ℹ️ {info.get('missed_dose', 'Take as soon as remembered')}")

    with oe:
        st.subheader("🍺 Alcohol Interaction")
        alcohol = info.get("alcohol", "Consult doctor")
        if "avoid" in alcohol.lower():
            st.error(f"🚫 {alcohol}")
        elif "safe" in alcohol.lower():
            st.success(f"✅ {alcohol}")
        else:
            st.warning(f"⚠️ {alcohol}")
