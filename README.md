# MedIntel AI — Intelligent Healthcare Assistant

MedIntel AI is a Streamlit-based healthcare assistant that analyzes medical reports, answers symptom queries, and provides medicine and diet guidance using a Retrieval-Augmented Generation (RAG) pipeline built on the Groq LLaMA 3.3 70B API. It combines LLM-based reasoning with a deterministic rule engine so that results remain available and bounded even when the AI call fails.

> **Disclaimer:** MedIntel AI is built for educational and informational purposes only. It is not a diagnostic tool and does not replace professional medical advice. Always consult a qualified healthcare provider for medical decisions.

---

## Overview

Most "AI health report analyzer" projects wrap a single LLM call around a PDF upload and call it done. MedIntel AI is built around three engineering decisions meant to make the AI output more trustworthy and more resilient:

1. **Hybrid scoring, not blind trust in the LLM.** Every report is scored twice — once by the Groq LLM and once by a deterministic, keyword-based rule engine (`health_engine.py`). The two scores are blended (75% AI / 25% rule-based), and if the LLM call fails outright, the system falls back entirely to the rule-based score rather than failing or hallucinating a result.
2. **A layered PDF/OCR pipeline**, not a single extraction method. Each page of an uploaded report is processed independently through a cascade — embedded PDF text → local OCR (RapidOCR) → Tesseract (if available) → Groq Vision as a last resort — so a single PDF containing both digital and scanned/photographed pages is still handled correctly, page by page.
3. **Domain-separated RAG.** Two independent TF-IDF knowledge bases (lab/report knowledge and drug knowledge) are indexed separately rather than merged, since mixing them would dilute retrieval quality for both — a term common in lab reports shouldn't influence drug-name matching, and vice versa.

---

## Features

### Medical Report Analyzer
- PDF upload with automatic report-type detection (12+ categories: CBC, lipid, diabetes, thyroid, kidney, liver, vitamins, urine, cardiac, radiology, hormone, infection)
- RAG-grounded analysis via Groq LLaMA 3.3 70B
- Health Score (0–100), blended from AI output and rule-based validation
- Risk level classification (Low / Moderate / High), reconciled against the blended score
- Abnormal test values with reference ranges
- Possible conditions, diet and exercise recommendations, and doctor follow-up advice
- Structured JSON output with response validation and fallback handling
- Auto-logged to the Health Dashboard

### Symptom Checker
RAG-enhanced symptom analysis producing possible conditions with likelihood, severity/urgency assessment, specialist recommendations, OTC suggestions, home remedies, and emergency warning signs.

### Medicine Guide
Lookup by Indian or international brand/generic name, backed by a curated drug knowledge base (drug class, uses, dosage considerations, interactions, contraindications).

### Diet Planner
BMI and calorie calculation from user inputs, with a personalized meal plan, foods to avoid, hydration guidance, and supplement notes.

### Health Dashboard
Auto-imported and manually logged reports, score trend and risk distribution charts, a vitals tracker (hemoglobin, cholesterol, blood sugar, TSH, creatinine, Vitamin D), and a daily vitals log.

---

## Architecture

```text
Upload PDF / Enter Symptoms / Search Medicine
                    │
                    ▼
        Text Extraction (utils.py)
  embedded text → RapidOCR → Tesseract → Groq Vision
                    │
                    ▼
     RAG Retrieval (rag_engine.py, TF-IDF)
   domain-separated: lab knowledge / drug knowledge
                    │
                    ▼
        Groq LLaMA 3.3 70B (analyzer.py)
       prompt grounded with retrieved context
                    │
                    ▼
   Rule-Based Cross-Check (health_engine.py)
     keyword/regex scoring, independent of the LLM
                    │
                    ▼
     Blend: 75% AI score + 25% rule score
        (falls back to 100% rule score on AI failure)
                    │
                    ▼
   Response Validation & Normalization (analyzer.py)
                    │
                    ▼
      Structured Result → UI + Health Dashboard
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI / App Framework | Streamlit |
| LLM Inference | Groq API — LLaMA 3.3 70B |
| Vision OCR Fallback | Groq API — LLaMA 4 Scout |
| Retrieval | Custom TF-IDF RAG (no external model download) |
| PDF Parsing | PyMuPDF (fitz) |
| Local OCR | RapidOCR, Tesseract (optional) |
| Data / Charts | Pandas, Plotly |
| Config | python-dotenv |

---

## Project Structure

```text
medintel-ai/
│
├── app.py                   # Entry point and page router
├── analyzer.py               # RAG-grounded report analysis + AI/rule blending
├── rag_engine.py              # TF-IDF retrieval (lab + drug knowledge, indexed separately)
├── knowledge_base.py           # Lab/condition knowledge chunks
├── drug_knowledge_base.py       # Medicine reference data
├── health_engine.py            # Rule-based scoring engine
├── dashboard_connector.py        # Converts analysis results into dashboard entries
├── utils.py                    # PDF extraction + OCR cascade + report-type detection
├── styles.py                   # Global theming
├── test_check.py               # Project health-check script (import/wiring smoke test)
├── requirements.txt
├── .env
│
├── pages/
│   ├── home.py
│   ├── report.py               # Report Analyzer
│   ├── symptom.py               # Symptom Checker
│   ├── medicine.py               # Medicine Guide
│   ├── diet.py                  # Diet Planner
│   ├── dashboard.py              # Health Dashboard
│   └── about.py
│
├── components/
│   ├── hero.py
│   ├── sidebar.py
│   └── cards.py
│
└── .streamlit/
    └── config.toml
```

---

## Installation

```bash
git clone https://github.com/yourusername/MedIntel-AI.git
cd MedIntel-AI
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

A free API key is available at [console.groq.com](https://console.groq.com).

Run the app:

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## Design Notes / Known Limitations

- The rule-based engine (`health_engine.py`) uses proximity-based keyword matching (test name within ~80 characters of a signal word like "high" or "low"). It's a fast, dependency-free sanity check on the LLM output — not a clinical scoring system — and can misfire on ambiguous report phrasing.
- `test_check.py` is a manual smoke-check script that verifies imports, wiring, and report-type detection; it is not a `pytest` suite.
- The AI/rule blend weighting (75/25) is a tunable constant in `blend_scores()`, chosen to favor contextual LLM understanding while keeping a deterministic floor.

---

## Roadmap

- [ ] Multi-language support
- [ ] Medical image analysis (X-ray/MRI interpretation)
- [ ] User authentication and persistent cloud storage
- [ ] Semantic RAG with vector embeddings (currently TF-IDF by design, to avoid model downloads)
- [ ] Wearable device integration

---

## Disclaimer

MedIntel AI provides AI-generated information for educational purposes only. It does not replace professional medical advice, diagnosis, or treatment. In case of emergency, contact local emergency services immediately.

---

## Author

**Sanskriti Agarwal**
B.Tech — Artificial Intelligence & Machine Learning

## License

MIT License
