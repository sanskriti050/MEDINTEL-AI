import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_medical_report(report_text: str, report_type: str) -> dict:
    """
    Send report text to Groq LLM and get structured medical analysis back.
    Handles any type of medical report PDF.
    """

    # Truncate extremely long reports to avoid token limits
    max_chars = 8000
    if len(report_text) > max_chars:
        report_text = report_text[:max_chars] + "\n... [report truncated for analysis]"

    prompt = f"""You are a senior physician and medical analyst with 25+ years of experience.

You have received a patient's {report_type}. Analyze it thoroughly.

STRICT RULES — follow every one:
1. Return ONLY a single valid JSON object. Nothing else.
2. No markdown. No ```json. No explanation text before or after the JSON.
3. Every field must have a value. Never use null or empty string for text fields.
4. "health_score" must be a plain integer between 0 and 100.
5. "risk_level" must be exactly one of these three words: Low  Moderate  High
6. "abnormal_values" — list every test result that is outside normal range. If all are normal, use [].
7. "possible_conditions" — list at least 3 possible diagnoses or health observations.
8. "diet" — list at least 5 specific dietary recommendations relevant to this report.
9. "exercise" — list at least 4 specific exercise recommendations.
10. "patient_summary" — write a full paragraph describing the patient's health status based on the report.
11. "doctor_advice" — write a detailed paragraph with specific follow-up instructions.

Return EXACTLY this JSON structure (no extra fields, no missing fields):

{{
  "patient_summary": "detailed paragraph about patient health status",
  "health_score": 80,
  "risk_level": "Low",
  "abnormal_values": [
    {{
      "test": "test name",
      "result": "patient value with unit",
      "status": "High / Low / Borderline",
      "normal_range": "reference range with unit"
    }}
  ],
  "possible_conditions": [
    "Condition 1 — brief explanation",
    "Condition 2 — brief explanation",
    "Condition 3 — brief explanation"
  ],
  "diet": [
    "Diet recommendation 1",
    "Diet recommendation 2",
    "Diet recommendation 3",
    "Diet recommendation 4",
    "Diet recommendation 5"
  ],
  "exercise": [
    "Exercise recommendation 1",
    "Exercise recommendation 2",
    "Exercise recommendation 3",
    "Exercise recommendation 4"
  ],
  "doctor_advice": "detailed follow-up paragraph"
}}

---
MEDICAL REPORT:
{report_text}
---"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.15,
            max_tokens=4000,
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical AI assistant. You ONLY output valid JSON. Never output markdown, explanations, or any text outside the JSON object."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content.strip()

        # Aggressively clean any markdown wrapping
        content = content.replace("```json", "").replace("```", "").strip()

        # Extract JSON object boundaries
        start = content.find("{")
        end = content.rfind("}") + 1

        if start == -1 or end <= 1:
            raise ValueError("No valid JSON object found in AI response")

        parsed = json.loads(content[start:end])

        # Sanitize and fill defaults
        parsed["health_score"] = max(0, min(100, int(parsed.get("health_score", 70))))

        risk = str(parsed.get("risk_level", "")).strip()
        if risk not in ("Low", "Moderate", "High"):
            # Try to auto-correct common variations
            risk_lower = risk.lower()
            if "low" in risk_lower:
                risk = "Low"
            elif "high" in risk_lower:
                risk = "High"
            else:
                risk = "Moderate"
        parsed["risk_level"] = risk

        # Ensure lists are lists
        for key in ("abnormal_values", "possible_conditions", "diet", "exercise"):
            if not isinstance(parsed.get(key), list):
                parsed[key] = []

        # Filter empty strings from lists
        for key in ("possible_conditions", "diet", "exercise"):
            parsed[key] = [item for item in parsed[key] if item and str(item).strip()]

        # Ensure abnormal_values items are dicts
        parsed["abnormal_values"] = [
            item for item in parsed["abnormal_values"]
            if isinstance(item, dict) and item.get("test")
        ]

        parsed.setdefault("patient_summary", "Analysis complete. Please review the details below.")
        parsed.setdefault("doctor_advice", "Please consult your physician for a thorough evaluation.")

        return parsed

    except json.JSONDecodeError as je:
        print(f"JSON Parse Error: {je}")
        print(f"Raw content was: {content[:500]}")
        return _fallback()
    except Exception as e:
        print(f"Groq Error: {e}")
        return _fallback()


def _fallback() -> dict:
    return {
        "patient_summary": "Analysis could not be completed due to a processing error. Please try again.",
        "health_score": 0,
        "risk_level": "Moderate",
        "abnormal_values": [],
        "possible_conditions": [],
        "diet": [],
        "exercise": [],
        "doctor_advice": "Please consult your healthcare provider for a thorough evaluation of this report."
    }
