# 🏥 MedIntel AI – Intelligent Healthcare Assistant

MedIntel AI is an AI-powered healthcare platform that helps users analyze medical reports, understand health conditions, receive personalized recommendations, and access essential healthcare tools through an interactive dashboard.

Built using **Python, Streamlit, Groq LLaMA 3.3 70B, RAG, SQLite, Plotly, and PyMuPDF**, the application provides fast, accurate, and user-friendly medical insights with a warm, modern interface.

> ⚠️ **Disclaimer:** MedIntel AI is designed for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.

---

## ✨ Features

### 📄 AI Medical Report Analyzer
- Upload any medical PDF (blood test, thyroid, lipid, kidney, liver, X-ray, etc.)
- Automatic report type detection (15+ report types supported)
- RAG-enhanced AI analysis using Groq LLaMA 3.3 70B
- Health Score (0–100) with interactive gauge chart
- Risk Level prediction — Low / Moderate / High
- Patient health summary paragraph
- Abnormal test value detection with normal ranges
- Possible medical conditions
- Personalized diet & exercise recommendations
- Doctor follow-up advice
- Downloadable JSON analysis report
- Auto-save to Health Dashboard

---

### 🩺 AI Symptom Checker
- Enter age, gender, symptoms, duration, existing conditions
- AI-powered possible condition list with likelihood (High / Moderate / Low)
- Severity and urgency assessment
- Recommended specialist type
- OTC medicine suggestions
- Home remedies
- Suggested diagnostic tests
- Emergency warning signs
- Lifestyle advice

---

### 💊 Medicine Guide
- Search any medicine — Indian brands (Dolo, Crocin, Augmentin) or international
- Generic name, manufacturer, drug class
- Mechanism of action
- Uses and indications
- Dosage guide (adult, child, frequency, max dose)
- Side effects (common, serious, rare)
- Contraindications and drug interactions
- Pregnancy & breastfeeding safety
- Overdose, missed dose, alcohol interaction info

---

### 🥗 Personal Diet Planner
- Input age, weight, height, gender, health goal, dietary preference
- BMI calculation and category
- Daily calorie target
- Personalized breakfast, lunch, dinner, snacks
- Foods to avoid
- Hydration advice
- Supplement recommendations
- Nutrition tips

---

### 📊 Health Dashboard
- Auto-import reports from Report Analyzer
- Manual report logging
- Health score trend chart
- Risk distribution pie chart
- Reports by type bar chart
- Full report history table
- Health vitals tracker (hemoglobin, cholesterol, blood sugar, TSH, creatinine, Vitamin D)
- Daily vitals log (BP, heart rate, SpO2, temperature, weight, water, sleep)
- Personal health profile with BMI gauge
- **Persistent storage — all data saved to local SQLite DB, survives browser refresh & restart**

---

## 🧠 RAG — Retrieval-Augmented Generation

MedIntel AI uses a **custom RAG pipeline** to improve AI analysis accuracy.

### How it works
```
User Input (report / symptoms / medicine)
          │
          ▼
TF-IDF Similarity Search
          │
          ▼
Top-5 Relevant Medical Knowledge Chunks Retrieved
          │
          ▼
Injected into Groq LLM Prompt
          │
          ▼
More Accurate, Fact-Grounded AI Response
```

### Knowledge Base covers
- 🩸 CBC / Blood tests — normal ranges, causes of abnormalities
- 🫀 Cholesterol / Lipid profile — risk levels, dietary guidance
- 🍬 Diabetes — HbA1c, fasting sugar, postprandial ranges
- 🦋 Thyroid — TSH, T3, T4 interpretation
- 🫘 Kidney function — Creatinine, BUN, eGFR
- 🟤 Liver function — ALT, AST, Bilirubin, ALP
- 💊 Vitamins & Minerals — D, B12, Iron, Calcium
- ❤️ Cardiovascular — BP, Troponin, heart health
- 🏃 General health — BMI, sleep, exercise, diet guidelines

### RAG Status
Visible in the sidebar — 🟢 **RAG Active** when running, showing chunk count and model info.
No model download required — uses lightweight TF-IDF retrieval.

---

## 🚀 Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Backend |
| Streamlit | Web Application UI |
| Groq API | AI inference engine |
| LLaMA 3.3 70B | Large Language Model |
| RAG (TF-IDF) | Retrieval-Augmented Generation |
| SQLite | Persistent local database (no install needed) |
| PyMuPDF (fitz) | PDF text extraction |
| RapidOCR | OCR for scanned PDFs |
| Groq Vision (LLaMA 4 Scout) | Vision OCR fallback |
| Plotly | Interactive charts |
| Pandas | Data processing |
| python-dotenv | Environment variables |

---

## 📂 Project Structure

```text
medintel-ai/
│
├── app.py                   # Main entry point
├── analyzer.py              # RAG-enhanced report analysis
├── rag_engine.py            # TF-IDF RAG retrieval engine
├── knowledge_base.py        # Medical knowledge chunks (54)
├── health_engine.py         # Rule-based health scoring + AI score blending
├── database.py              # SQLite persistence layer (reports, vitals, profile)
├── dashboard_connector.py   # Auto-save reports to dashboard + DB
├── utils.py                 # PDF extraction + OCR pipeline
├── styles.py                # Global CSS theming
├── requirements.txt
├── .env
│
├── pages/
│   ├── home.py              # Landing page
│   ├── report.py            # Medical Report Analyzer
│   ├── symptom.py           # Symptom Checker (RAG-enhanced)
│   ├── medicine.py          # Medicine Guide (RAG-enhanced)
│   ├── diet.py              # Diet Planner
│   ├── dashboard.py         # Health Dashboard (SQLite-backed)
│   └── about.py             # About page
│
├── components/
│   ├── hero.py              # Hero section component
│   ├── sidebar.py           # Sidebar component
│   └── cards.py             # Card components
│
└── .streamlit/
    └── config.toml          # Streamlit theme config
```

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/MedIntel-AI.git
cd MedIntel-AI
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables**

Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key at [console.groq.com](https://console.groq.com)

---

## ▶️ Run the Project

```bash
streamlit run app.py
```

The application will open automatically at `http://localhost:8501`

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Groq API key for LLM inference | ✅ Yes |

---

## 🧠 Full AI Workflow

```text
Upload PDF / Enter Symptoms / Search Medicine
          │
          ▼
Text Extraction (PyMuPDF → RapidOCR → Groq Vision)
          │
          ▼
RAG: TF-IDF retrieval from 54 medical knowledge chunks
          │
          ▼
Groq LLaMA 3.3 70B Analysis (with RAG context injected)
          │
          ▼
Rule-based Health Engine cross-check (35+ scoring rules)
          │
          ▼
AI Score (75%) + Rule Score (25%) blended → Final Health Score
          │
          ▼
Structured JSON response parsed & validated
          │
          ▼
Health Score + Risk Level + Insights displayed
          │
          ▼
Auto-saved to Health Dashboard
```

---

## 📊 Supported Report Types

| Report Type | Key Tests Detected |
|---|---|
| Blood / CBC | Hemoglobin, WBC, RBC, Platelets, MCV |
| Lipid Profile | Cholesterol, LDL, HDL, Triglycerides |
| Diabetes | Glucose, HbA1c, Fasting Sugar, PPBS |
| Thyroid | TSH, T3, T4, Free T3, Free T4 |
| Kidney Function | Creatinine, BUN, eGFR, Uric Acid |
| Liver Function | ALT, AST, Bilirubin, ALP, Albumin |
| Vitamin Profile | Vitamin D, B12, Iron, Calcium, Zinc |
| Urine Analysis | Routine urine, pus cells |
| Cardiac | ECG, Troponin, Echocardiogram |
| Radiology | X-ray, MRI, CT Scan, Ultrasound |
| Hormone Profile | Testosterone, Estrogen, Cortisol, FSH |
| Infection | CRP, ESR, Dengue, HIV, Hepatitis |

---

## 🔮 Future Enhancements

- [ ] Multi-language support (Hindi, regional languages)
- [ ] Voice-based symptom input
- [ ] Medical image analysis (X-ray, MRI interpretation)
- [ ] Authentication system with user accounts
- [x] Local SQLite database for persistent health history
- [ ] Cloud database for multi-device sync
- [ ] Wearable device integration
- [ ] Appointment booking system
- [ ] WhatsApp / Telegram health bot
- [ ] Semantic RAG with vector embeddings (when disk space available)

---

## 🛡️ Disclaimer

MedIntel AI provides AI-generated healthcare information intended for **educational and informational purposes only**.

- Does **not** replace professional medical advice, diagnosis, or treatment
- Always consult a qualified healthcare professional for medical decisions
- In case of emergency, contact local emergency services immediately

---

## 👩‍💻 Author

**Sanskriti Agarwal**  
B.Tech – Artificial Intelligence & Machine Learning  
Full Stack & AI Developer

---

## ⭐ Support

If you found this project useful, give it a ⭐ on GitHub — it helps and motivates future development!

---

## 📜 License

This project is licensed under the **MIT License**.
