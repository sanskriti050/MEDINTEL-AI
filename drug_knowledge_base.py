"""
Drug Knowledge Base for RAG (Medicine Guide)
──────────────────────────────────────────────
Curated facts about common medicines — brand names, generic names,
drug class, and core uses. Used to ground the Medicine Guide's AI
responses in reference data, separate from the lab-report knowledge
base in knowledge_base.py (that one covers test values/conditions,
not drug information — the two domains don't overlap).

Each entry includes common Indian brand names AND the generic name,
so a query for either ("Dolo 650" or "Paracetamol") can match.
"""

DRUG_KNOWLEDGE = [
    {
        "brand_names": ["Dolo 650", "Crocin", "Calpol", "Tylenol"],
        "generic_name": "Paracetamol (Acetaminophen)",
        "drug_class": "Analgesic / Antipyretic",
        "common_uses": "Fever reduction, mild to moderate pain relief (headache, body ache, toothache).",
        "key_notes": "Generally safe OTC drug. Max daily dose ~3-4g for adults. Overdose can cause severe liver damage — avoid combining multiple paracetamol-containing products."
    },
    {
        "brand_names": ["Combiflam", "Brufen", "Advil", "Motrin"],
        "generic_name": "Ibuprofen (often combined with Paracetamol in Combiflam)",
        "drug_class": "NSAID (Non-Steroidal Anti-Inflammatory Drug)",
        "common_uses": "Pain relief, inflammation reduction, fever, arthritis, muscle pain.",
        "key_notes": "Avoid in kidney disease, active stomach ulcers, or late pregnancy. Take with food to reduce stomach irritation. Avoid combining with other NSAIDs."
    },
    {
        "brand_names": ["Augmentin", "Clavam", "Moxikind-CV"],
        "generic_name": "Amoxicillin + Clavulanic Acid",
        "drug_class": "Antibiotic (Penicillin group, beta-lactamase inhibitor combination)",
        "common_uses": "Bacterial infections — respiratory tract, urinary tract, skin, dental infections.",
        "key_notes": "Complete the full prescribed course even if symptoms improve. Common side effect: diarrhea, nausea. Avoid if allergic to penicillin."
    },
    {
        "brand_names": ["Metrogyl", "Flagyl"],
        "generic_name": "Metronidazole",
        "drug_class": "Antibiotic / Antiprotozoal",
        "common_uses": "Anaerobic bacterial infections, protozoal infections (amoebiasis, giardiasis), dental infections.",
        "key_notes": "Strictly avoid alcohol during and 48 hours after treatment — causes severe nausea/vomiting (disulfiram-like reaction)."
    },
    {
        "brand_names": ["Pantop", "Pan 40", "Protonix"],
        "generic_name": "Pantoprazole",
        "drug_class": "Proton Pump Inhibitor (PPI)",
        "common_uses": "Acid reflux, GERD, stomach ulcers, heartburn.",
        "key_notes": "Best taken on empty stomach, 30-60 min before breakfast. Long-term use may reduce Vitamin B12 and magnesium absorption."
    },
    {
        "brand_names": ["Shelcal", "Shelcal 500", "Calcirol"],
        "generic_name": "Calcium Carbonate + Vitamin D3",
        "drug_class": "Calcium & Vitamin D Supplement",
        "common_uses": "Calcium deficiency, bone health support, osteoporosis prevention.",
        "key_notes": "Take with food for better absorption. Avoid taking at the same time as iron supplements or certain antibiotics (reduces absorption of both)."
    },
    {
        "brand_names": ["Revital", "Revital H"],
        "generic_name": "Multivitamin + Multimineral + Ginseng blend",
        "drug_class": "Dietary Supplement",
        "common_uses": "General nutritional support, energy, immunity support.",
        "key_notes": "Not a substitute for a balanced diet. Consult a doctor before combining with other supplements to avoid excess vitamin/mineral intake."
    },
    {
        "brand_names": ["Azithral", "Zithromax", "Azee"],
        "generic_name": "Azithromycin",
        "drug_class": "Antibiotic (Macrolide)",
        "common_uses": "Respiratory infections, ear infections, skin infections, typhoid, some STIs.",
        "key_notes": "Usually a short 3-5 day course due to long half-life. Take on empty stomach for best absorption. Can affect heart rhythm in rare cases — caution with existing cardiac conditions."
    },
    {
        "brand_names": ["Cifran", "Ciplox", "Cipro"],
        "generic_name": "Ciprofloxacin",
        "drug_class": "Antibiotic (Fluoroquinolone)",
        "common_uses": "Urinary tract infections, gastrointestinal infections, some respiratory infections.",
        "key_notes": "Avoid dairy products and antacids near dosing time (reduces absorption). Rare risk of tendon damage, especially in older adults."
    },
    {
        "brand_names": ["Glycomet", "Glucophage"],
        "generic_name": "Metformin",
        "drug_class": "Biguanide (Anti-diabetic)",
        "common_uses": "First-line treatment for Type 2 diabetes, helps control blood sugar.",
        "key_notes": "Take with meals to reduce GI upset (common side effect). Can cause Vitamin B12 deficiency with long-term use — periodic monitoring recommended."
    },
    {
        "brand_names": ["Atorva", "Lipitor"],
        "generic_name": "Atorvastatin",
        "drug_class": "Statin (Lipid-lowering agent)",
        "common_uses": "Lowering LDL cholesterol, reducing cardiovascular disease risk.",
        "key_notes": "Usually taken at night. Rare but notable side effect: muscle pain/weakness (report to doctor if severe). Avoid grapefruit juice — increases drug levels."
    },
    {
        "brand_names": ["Alprax", "Xanax"],
        "generic_name": "Alprazolam",
        "drug_class": "Benzodiazepine (Anxiolytic)",
        "common_uses": "Short-term treatment of anxiety disorders, panic attacks.",
        "key_notes": "Prescription-only, habit-forming with prolonged use. Never stop abruptly after regular use — requires tapering. Avoid alcohol."
    },
    {
        "brand_names": ["Nexpro", "Nexium"],
        "generic_name": "Esomeprazole",
        "drug_class": "Proton Pump Inhibitor (PPI)",
        "common_uses": "GERD, acid reflux, stomach ulcer treatment/prevention.",
        "key_notes": "Similar profile to Pantoprazole. Best on empty stomach before a meal. Long-term use monitored for bone density/nutrient absorption effects."
    },
    {
        "brand_names": ["Zincovit", "Zinconia"],
        "generic_name": "Zinc (various salts) often combined with multivitamins",
        "drug_class": "Mineral Supplement",
        "common_uses": "Immune support, wound healing support, zinc deficiency correction.",
        "key_notes": "Excess zinc can interfere with copper absorption. Take with food to reduce nausea."
    },
    {
        "brand_names": ["Cetzine", "Zyrtec"],
        "generic_name": "Cetirizine",
        "drug_class": "Antihistamine (2nd generation)",
        "common_uses": "Allergic rhinitis, hives, itching, seasonal allergy symptoms.",
        "key_notes": "Less sedating than older antihistamines but can still cause mild drowsiness in some. Generally safe OTC option."
    },
    {
        "brand_names": ["Omnacortil", "Wysolone"],
        "generic_name": "Prednisolone",
        "drug_class": "Corticosteroid",
        "common_uses": "Inflammation control — allergies, asthma flare-ups, autoimmune conditions.",
        "key_notes": "Never stop abruptly after prolonged use — requires tapering under doctor supervision. Long-term use has significant side effects (weight gain, bone loss, blood sugar rise)."
    },
]