import streamlit as st
import os
import json
from components.hero import show_hero, show_notice
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def get_diet_plan(age: int, gender: str, weight: float, height: float,
                  goal: str, conditions: str, dietary_pref: str) -> dict:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    bmi = round(weight / ((height / 100) ** 2), 1)

    prompt = f"""
You are a certified nutritionist. Create a personalized diet plan for:

Patient Profile:
- Age: {age}
- Gender: {gender}
- Weight: {weight} kg
- Height: {height} cm
- BMI: {bmi}
- Goal: {goal}
- Medical Conditions: {conditions if conditions else "None"}
- Dietary Preference: {dietary_pref}

Return ONLY valid JSON in this exact format:

{{
    "bmi": {bmi},
    "bmi_category": "",
    "daily_calories": 2000,
    "breakfast": ["item1", "item2"],
    "lunch": ["item1", "item2"],
    "dinner": ["item1", "item2"],
    "snacks": ["item1", "item2"],
    "foods_to_avoid": ["item1", "item2"],
    "hydration": "",
    "supplements": ["supplement1"],
    "tips": ["tip1", "tip2"]
}}

Rules:
- Return ONLY JSON. No markdown. No explanation.
- daily_calories must be a number.
- All meal fields must be lists of strings.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip()
        if "```" in content:
            content = content.replace("```json", "").replace("```", "").strip()
        start = content.find("{")
        end = content.rfind("}") + 1
        return json.loads(content[start:end])
    except Exception as e:
        print("Groq Error:", e)
        return {
            "bmi": bmi,
            "bmi_category": "Unknown",
            "daily_calories": 2000,
            "breakfast": ["Oats with fruits", "Green tea"],
            "lunch": ["Brown rice", "Vegetables", "Dal"],
            "dinner": ["Roti", "Sabzi", "Curd"],
            "snacks": ["Fruits", "Nuts"],
            "foods_to_avoid": ["Processed foods", "Sugary drinks"],
            "hydration": "Drink 8-10 glasses of water daily",
            "supplements": ["Consult doctor"],
            "tips": ["Eat on time", "Avoid late night eating"]
        }


def show_diet():
    show_hero("🥗 Personal Diet Planner", "Create a practical food plan around your body, lifestyle and health goal.", "NUTRITION, MADE PERSONAL")
    show_notice("Built around you", "Add your basic details below and receive a structured daily plan in seconds.", "✨")
    st.markdown("### Your nutrition profile")

    with st.form("diet_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("🔢 Age", min_value=1, max_value=120, value=25)
            weight = st.number_input("⚖️ Weight (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.5)
            goal = st.selectbox("🎯 Health Goal", [
                "Weight Loss", "Weight Gain", "Maintain Weight",
                "Muscle Building", "General Health", "Manage Diabetes",
                "Heart Health", "Boost Immunity"
            ])
            conditions = st.text_input("🏥 Medical Conditions (if any)", placeholder="e.g. Diabetes, Hypertension")

        with col2:
            gender = st.selectbox("⚧ Gender", ["Male", "Female", "Other"])
            height = st.number_input("📏 Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.5)
            dietary_pref = st.selectbox("🌿 Dietary Preference", [
                "Non-Vegetarian", "Vegetarian", "Vegan", "Eggetarian", "Keto", "Gluten-Free"
            ])

        submitted = st.form_submit_button("🥗 Generate Diet Plan", use_container_width=True)

    if submitted:
        bmi_display = round(weight / ((height / 100) ** 2), 1)

        with st.spinner("AI is creating your personalized diet plan..."):
            plan = get_diet_plan(age, gender, weight, height, goal, conditions, dietary_pref)

        st.success("✅ Your Personalized Diet Plan is Ready!")
        st.divider()

        # BMI display
        col1, col2, col3 = st.columns(3)
        col1.metric("📊 Your BMI", plan.get("bmi", bmi_display))
        col2.metric("🏷️ BMI Category", plan.get("bmi_category", "N/A"))
        col3.metric("🔥 Daily Calories", f"{plan.get('daily_calories', 2000)} kcal")

        st.divider()

        # Meals
        col4, col5, col6 = st.columns(3)

        with col4:
            st.subheader("🌅 Breakfast")
            for item in plan.get("breakfast", []):
                st.success(f"🍽️ {item}")

        with col5:
            st.subheader("☀️ Lunch")
            for item in plan.get("lunch", []):
                st.success(f"🍽️ {item}")

        with col6:
            st.subheader("🌙 Dinner")
            for item in plan.get("dinner", []):
                st.success(f"🍽️ {item}")

        st.divider()

        col7, col8 = st.columns(2)

        with col7:
            st.subheader("🍎 Snacks")
            for item in plan.get("snacks", []):
                st.info(f"🍎 {item}")

            st.subheader("💧 Hydration")
            st.info(plan.get("hydration", "Drink plenty of water"))

        with col8:
            st.subheader("🚫 Foods to Avoid")
            for item in plan.get("foods_to_avoid", []):
                st.error(f"❌ {item}")

            st.subheader("💊 Supplements")
            for sup in plan.get("supplements", []):
                st.warning(f"💊 {sup}")

        st.divider()
        st.subheader("💡 Nutrition Tips")
        for tip in plan.get("tips", []):
            st.info(f"✅ {tip}")
