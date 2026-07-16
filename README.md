# 🏥 MedIntel AI – Intelligent Healthcare Assistant

MedIntel AI is an AI-powered healthcare platform that helps users analyze medical reports, understand health conditions, receive personalized recommendations, and access essential healthcare tools through an interactive dashboard.

Built using **Python, Streamlit, Groq Llama 3.3 70B, Plotly, and PyMuPDF**, the application provides fast and user-friendly medical insights with an intuitive interface.

> ⚠️ **Disclaimer:** MedIntel AI is designed for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.

---

# ✨ Features

## 📄 AI Medical Report Analyzer

- Upload Medical Reports (PDF)
- Automatic Report Type Detection
- AI-Powered Medical Report Analysis
- Health Score (0–100)
- Risk Level Prediction
- Patient Health Summary
- Abnormal Test Detection
- Possible Medical Conditions
- Diet Recommendations
- Exercise Recommendations
- Doctor Advice
- Interactive Health Score Gauge
- Health Score Pie Chart
- Download AI Analysis Report

---

## 🩺 AI Symptom Checker

- Describe Symptoms
- AI-Based Possible Conditions
- Severity Assessment
- Home Care Suggestions
- When to Visit a Doctor
- Emergency Warning Detection

---

## 💊 Medicine Explainer

- Search Medicines
- Medicine Uses
- Dosage Information
- Side Effects
- Precautions
- Drug Safety Tips

---

## 🥗 Diet Planner

- Personalized Diet Suggestions
- Healthy Food Recommendations
- Nutrition Tips
- Hydration Advice
- Lifestyle Recommendations

---

## 📊 Health Dashboard

- Previous Report Statistics
- Overall Health Score
- Risk Summary
- Interactive Charts
- AI Health Insights

---

# 🚀 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Streamlit | Web Application |
| Groq API | AI Medical Analysis |
| Llama 3.3 70B | Large Language Model |
| PyMuPDF (fitz) | PDF Text Extraction |
| Plotly | Interactive Charts |
| Pandas | Data Processing |
| Python Dotenv | Environment Variables |

---

# 📂 Project Structure

```text
MedIntel-AI/
│
├── app.py
├── analyzer.py
├── utils.py
├── styles.py
├── requirements.txt
├── .env
│
├── pages/
│   ├── home.py
│   ├── report.py
│   ├── symptom.py
│   ├── medicine.py
│   ├── diet.py
│   ├── dashboard.py
│   └── about.py
│
└── assets/
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/MedIntel-AI.git
```

Move into the project folder

```bash
cd MedIntel-AI
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file inside the project folder.

```env
GROQ_API_KEY=your_groq_api_key
```

---

# ▶️ Run the Project

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

# 🧠 AI Workflow

```text
Upload Medical Report
          │
          ▼
PDF Text Extraction
          │
          ▼
Report Type Detection
          │
          ▼
Groq Llama 3.3 Analysis
          │
          ▼
Health Score Generation
          │
          ▼
Medical Insights
          │
          ▼
Dashboard Visualization
```

---

# 📊 AI Report Includes

- Patient Summary
- Health Score
- Risk Level
- Abnormal Tests
- Possible Conditions
- Diet Plan
- Exercise Plan
- Doctor Advice
- Interactive Charts
- Downloadable Report

---

# 📸 Screenshots

Add screenshots of:

- 🏠 Home Page
- 📄 Medical Report Analyzer
- 🩺 Symptom Checker
- 💊 Medicine Guide
- 🥗 Diet Planner
- 📊 Dashboard

---

# 🔮 Future Enhancements

- OCR Support for Scanned Reports
- Medical Image Analysis
- Disease Prediction Models
- Voice-Based Health Assistant
- Appointment Booking
- Health History Tracking
- Multi-Language Support
- Wearable Device Integration
- Cloud Database Support
- Authentication System

---

# 🛡 Disclaimer

MedIntel AI provides AI-generated healthcare information intended for educational purposes only.

Always consult a qualified healthcare professional before making any medical decisions.

---

# 👩‍💻 Author

**Sanskriti Agarwal**

B.Tech – Artificial Intelligence & Machine Learning

Full Stack & AI Developer

GitHub: https://github.com/yourusername

LinkedIn: https://linkedin.com/in/yourprofile

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

Your support helps improve the project and motivates future development.

---

## 📜 License

This project is licensed under the **MIT License**.
