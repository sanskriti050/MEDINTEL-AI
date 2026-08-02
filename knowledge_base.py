"""
Medical Knowledge Base for RAG (Retrieval-Augmented Generation)
Contains curated medical facts used to enrich AI analysis context.
"""

MEDICAL_KNOWLEDGE = [

    # ── Blood / CBC ────────────────────────────────────────────────────────
    "Hemoglobin normal range: Men 13.5–17.5 g/dL, Women 12.0–15.5 g/dL. Low hemoglobin indicates anemia. Causes include iron deficiency, B12 deficiency, chronic disease, or blood loss.",
    "Low hemoglobin (anemia) symptoms: fatigue, weakness, pale skin, shortness of breath, dizziness. Iron-rich foods like spinach, lentils, red meat, and fortified cereals are recommended.",
    "High WBC (leukocytosis) above 11,000/uL may indicate bacterial infection, inflammation, leukemia, or stress response. Requires further investigation with differential count.",
    "Low WBC (leukopenia) below 4,000/uL may indicate viral infections, bone marrow disorders, autoimmune conditions, or medication side effects.",
    "Platelet count normal: 150,000–400,000/uL. Low platelets (thrombocytopenia) risk: dengue fever, ITP, liver disease. High platelets may indicate infection or iron deficiency.",
    "RBC normal range: Men 4.5–5.9 million/uL, Women 4.1–5.1 million/uL. Low RBC with low hemoglobin confirms anemia.",
    "MCV (Mean Corpuscular Volume) normal 80–100 fL. Low MCV = microcytic anemia (iron deficiency). High MCV = macrocytic anemia (B12/folate deficiency).",

    # ── Lipid / Cholesterol ────────────────────────────────────────────────
    "Total cholesterol below 200 mg/dL is desirable. 200–239 borderline high. Above 240 is high risk for cardiovascular disease.",
    "LDL cholesterol (bad cholesterol) should be below 100 mg/dL ideally. Above 160 mg/dL is high risk. LDL reduction reduces heart attack risk significantly.",
    "HDL cholesterol (good cholesterol) above 60 mg/dL is protective. Below 40 mg/dL in men and 50 mg/dL in women increases cardiovascular risk.",
    "Triglycerides normal below 150 mg/dL. 150–199 borderline. Above 200 high. Above 500 very high, risk of pancreatitis. Reduce sugar, alcohol, refined carbs.",
    "High cholesterol diet recommendations: avoid saturated fats, trans fats, fried food. Eat oats, fish, nuts, olive oil, fruits and vegetables. Exercise 30 min/day.",

    # ── Diabetes / Blood Sugar ─────────────────────────────────────────────
    "Fasting blood glucose normal: 70–99 mg/dL. 100–125 prediabetes. Above 126 mg/dL on two tests confirms diabetes.",
    "HbA1c normal below 5.7%. 5.7–6.4% prediabetes. Above 6.5% indicates diabetes. HbA1c reflects average blood sugar over 3 months.",
    "Diabetes management: low glycemic index diet, regular exercise, weight management, avoid sugary drinks. Monitor blood sugar regularly. Medications may include Metformin.",
    "Postprandial blood sugar (2 hours after meal) normal below 140 mg/dL. 140–199 impaired glucose tolerance. Above 200 indicates diabetes.",
    "Diabetic patients should eat: whole grains, legumes, vegetables, lean protein. Avoid white rice, white bread, sugary foods, sweetened beverages.",

    # ── Thyroid ────────────────────────────────────────────────────────────
    "TSH (Thyroid Stimulating Hormone) normal range: 0.4–4.0 mIU/L. High TSH indicates hypothyroidism. Low TSH indicates hyperthyroidism.",
    "Hypothyroidism symptoms: fatigue, weight gain, constipation, cold intolerance, dry skin, depression. Treated with Levothyroxine.",
    "Hyperthyroidism symptoms: weight loss, rapid heartbeat, anxiety, sweating, tremors, heat intolerance. Treated with antithyroid drugs or radioiodine.",
    "T3 (Triiodothyronine) normal: 80–200 ng/dL. T4 (Thyroxine) normal: 5.0–12.0 ug/dL. Free T4 normal: 0.8–1.8 ng/dL.",
    "Thyroid patients should avoid excessive iodine, raw goitrogenic vegetables like cabbage and broccoli in large amounts. Soy may interfere with thyroid medication absorption.",

    # ── Kidney Function ────────────────────────────────────────────────────
    "Creatinine normal: Men 0.7–1.3 mg/dL, Women 0.6–1.1 mg/dL. High creatinine indicates reduced kidney function or dehydration.",
    "Blood Urea Nitrogen (BUN) normal: 7–20 mg/dL. High BUN suggests kidney disease, dehydration, or high protein intake.",
    "eGFR (estimated Glomerular Filtration Rate) above 90 mL/min/1.73m² is normal. 60–89 mild decrease. Below 60 indicates chronic kidney disease.",
    "Kidney disease diet: limit protein, sodium, potassium, phosphorus. Avoid NSAIDs like ibuprofen. Stay well hydrated unless told to restrict fluids.",
    "Uric acid normal: Men 3.4–7.0 mg/dL, Women 2.4–6.0 mg/dL. High uric acid causes gout. Avoid red meat, organ meats, shellfish, beer.",

    # ── Liver Function ─────────────────────────────────────────────────────
    "ALT (SGPT) normal: 7–56 U/L. AST (SGOT) normal: 10–40 U/L. Elevated liver enzymes indicate hepatitis, fatty liver, or alcohol damage.",
    "Bilirubin total normal: 0.2–1.2 mg/dL. High bilirubin causes jaundice. Indicates liver disease, bile duct obstruction, or hemolysis.",
    "Alkaline Phosphatase (ALP) normal: 44–147 U/L. Elevated in liver disease, bone disorders, bile duct obstruction.",
    "Fatty liver disease: reduce alcohol, lose weight, eat Mediterranean diet, avoid processed foods. Regular exercise helps reverse early fatty liver.",
    "Albumin normal: 3.5–5.0 g/dL. Low albumin indicates malnutrition, liver disease, or kidney disease causing protein loss.",

    # ── Vitamins & Minerals ────────────────────────────────────────────────
    "Vitamin D normal: 30–100 ng/mL. Deficiency below 20 ng/mL causes bone weakness, muscle pain, immune dysfunction, depression.",
    "Vitamin D deficiency is extremely common in India. Recommended: 15–20 minutes sunlight daily, fatty fish, egg yolks, fortified milk. Supplement: Vitamin D3 1000–2000 IU/day.",
    "Vitamin B12 normal: 200–900 pg/mL. Deficiency causes megaloblastic anemia, neurological damage, fatigue, tingling in hands and feet. Common in vegetarians.",
    "Iron normal: Men 65–176 ug/dL, Women 50–170 ug/dL. Ferritin normal: 12–300 ng/mL (men), 12–150 ng/mL (women). Low iron causes anemia.",
    "Calcium normal: 8.5–10.5 mg/dL. Low calcium causes muscle cramps, bone weakness. Sources: dairy, leafy greens, almonds, sesame seeds.",

    # ── Cardiovascular ─────────────────────────────────────────────────────
    "Normal blood pressure: below 120/80 mmHg. Hypertension stage 1: 130–139/80–89. Stage 2: above 140/90. Hypertensive crisis: above 180/120.",
    "High blood pressure management: DASH diet, reduce sodium below 2300mg/day, exercise regularly, reduce stress, limit alcohol, quit smoking.",
    "Troponin I and T elevated above 0.04 ng/mL suggests myocardial injury or heart attack. Requires immediate medical attention.",
    "Heart disease prevention: Mediterranean diet, 150 min moderate exercise per week, maintain healthy weight, no smoking, manage stress.",

    # ── Common Conditions ──────────────────────────────────────────────────
    "Iron deficiency anemia is the most common nutritional deficiency worldwide. Treatment: iron supplements, iron-rich diet. Vitamin C enhances iron absorption.",
    "Metabolic syndrome: combination of high blood sugar, high cholesterol, high blood pressure, and abdominal obesity. Major risk factor for heart disease and diabetes.",
    "PCOD/PCOS symptoms include irregular periods, high androgens, insulin resistance. Diet: low GI foods, regular exercise, weight management.",
    "Inflammation markers: CRP (C-Reactive Protein) above 3 mg/L indicates systemic inflammation. ESR elevated in infections, autoimmune disorders.",
    "Dengue: platelet count drops rapidly. Monitor daily. Platelet transfusion needed below 10,000/uL. Stay hydrated, papaya leaf extract may help.",

    # ── General Health ─────────────────────────────────────────────────────
    "Regular health checkup parameters: CBC, lipid profile, blood sugar, thyroid, kidney function, liver function, Vitamin D, B12 — annually for adults above 30.",
    "BMI normal range: 18.5–24.9 kg/m². Overweight 25–29.9. Obese above 30. Asian cutoffs are lower: overweight above 23, obese above 27.5.",
    "Sleep 7–9 hours per night is essential for immune function, hormone regulation, mental health, and cardiovascular health.",
    "Physical activity recommendations: 150 minutes moderate aerobic activity or 75 minutes vigorous activity per week plus muscle strengthening twice a week.",
    "Mediterranean diet components: olive oil, fish, whole grains, legumes, nuts, vegetables, fruits. Associated with lower rates of heart disease, diabetes, and cancer.",
    "Gut health: probiotics in yogurt, fermented foods support microbiome. Fiber from vegetables, fruits, whole grains promotes healthy digestion.",
    "Stress and cortisol: chronic stress elevates cortisol causing weight gain, high blood pressure, immune suppression, poor sleep. Yoga, meditation, exercise help.",
    "Hydration: 8–10 glasses water daily. Dehydration causes headache, fatigue, kidney stones, constipation. Monitor urine color — pale yellow is ideal.",
]
