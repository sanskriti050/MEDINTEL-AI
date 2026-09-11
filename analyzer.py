"""
analyzer.py
───────────
RAG-enhanced medical report analysis using Groq LLaMA 3.3 70B.

Flow
────
1. Retrieve relevant medical knowledge via TF-IDF RAG.
2. Send report text + RAG context to Groq LLM.
3. Parse & validate the structured JSON response.
4. Cross-check the AI health score with the rule-based health_engine.
   • If the AI call succeeds  → blend AI score (75 %) + rule score (25 %).
   • If the AI call fails     → fall back entirely to the rule-based score.
5. Return a validated dict ready for the UI.
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq

from health_engine import calculate_health_score, blend_scores   # ← health_engine now used
from config import get_groq_api_key

load_dotenv()

client = Groq(api_key=get_groq_api_key())


# ─────────────────────────────────────────────────────────────────────────────
def analyze_medical_report(report_text: str, report_type: str) -> dict:
    """
    Analyze a medical report using RAG-enhanced Groq LLM with a rule-based
    health_engine cross-check.

    Parameters
    ----------
    report_text : str   Raw text extracted from the PDF.
    report_type : str   Detected report type label.

    Returns
    -------
    dict  Validated analysis dict with keys:
          patient_summary, health_score, risk_level, abnormal_values,
          possible_conditions, diet, exercise, doctor_advice
    """

    # ── 1. Rule-based baseline (always computed, used as fallback / blend) ──
    rule_score, rule_risk, rule_abnormals = calculate_health_score(report_text)

    # ── 2. Truncate very long reports to stay within token limits ────────────
    max_chars = 8000
    if len(report_text) > max_chars:
        report_text = report_text[:max_chars] + "\n... [report truncated for analysis]"

    # ── 3. RAG: retrieve relevant medical knowledge chunks ───────────────────
    rag_context = ""
    try:
        from rag_engine import retrieve_relevant_context
        rag_context = retrieve_relevant_context(report_text, top_k=6)
    except Exception as e:
        print(f"[RAG] Skipped: {e}")

    # ── 4. Build the LLM prompt ──────────────────────────────────────────────
    prompt = f"""You are a senior physician and medical analyst with 25+ years of experience.

You have received a patient's {report_type}. Analyze it thoroughly.
{rag_context}
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
10. "patient_summary" — write a full paragraph describing the patient's health status.
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

    # ── 5. Call Groq LLM ─────────────────────────────────────────────────────
    try:
        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            temperature=0.15,
            max_tokens=4000,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a medical AI assistant. "
                        "You ONLY output valid JSON. "
                        "Never output markdown, explanations, or any text outside the JSON object."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )

        content = response.choices[0].message.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()

        start = content.find("{")
        end   = content.rfind("}") + 1

        if start == -1 or end <= 1:
            raise ValueError("No valid JSON object found in AI response")

        parsed = json.loads(content[start:end])

        # ── 6. Validate & normalise AI response ──────────────────────────────
        ai_score = max(0, min(100, int(parsed.get("health_score", rule_score))))

        risk = str(parsed.get("risk_level", "")).strip()
        if risk not in ("Low", "Moderate", "High"):
            risk_lower = risk.lower()
            if "low" in risk_lower:
                risk = "Low"
            elif "high" in risk_lower:
                risk = "High"
            else:
                risk = "Moderate"

        for key in ("abnormal_values", "possible_conditions", "diet", "exercise"):
            if not isinstance(parsed.get(key), list):
                parsed[key] = []

        for key in ("possible_conditions", "diet", "exercise"):
            parsed[key] = [item for item in parsed[key] if item and str(item).strip()]

        parsed["abnormal_values"] = [
            item for item in parsed["abnormal_values"]
            if isinstance(item, dict) and item.get("test")
        ]

        parsed.setdefault(
            "patient_summary",
            "Analysis complete. Please review the details below.",
        )
        parsed.setdefault(
            "doctor_advice",
            "Please consult your physician for a thorough evaluation.",
        )

        # ── 7. Blend AI score with rule-based score (75 % AI, 25 % rule) ────
        final_score = blend_scores(ai_score, rule_score, weight_ai=0.75)
        parsed["health_score"] = final_score

        # Re-derive risk from blended score if AI risk contradicts it clearly
        if final_score >= 75 and risk == "High":
            risk = "Moderate"
        elif final_score < 40 and risk == "Low":
            risk = "Moderate"
        parsed["risk_level"] = risk

        return parsed

    except json.JSONDecodeError as je:
        print(f"[Analyzer] JSON parse error: {je}")
        return _rule_fallback(rule_score, rule_risk, rule_abnormals)

    except Exception as e:
        print(f"[Analyzer] Groq error: {e}")
        return _rule_fallback(rule_score, rule_risk, rule_abnormals)


# ─────────────────────────────────────────────────────────────────────────────
def _rule_fallback(score: int, risk: str, abnormals: list[str]) -> dict:
    """
    Return a minimal but non-empty result built entirely from the
    rule-based health engine when the LLM call fails.
    """
    # Convert rule abnormal strings to the standard dict format
    abnormal_values = [
        {"test": a.split(" → ")[0], "result": "Abnormal",
         "status": a.split(" → ")[1] if " → " in a else "Abnormal",
         "normal_range": "See lab reference ranges"}
        for a in abnormals
    ]

    conditions = ["Unable to determine — AI analysis failed. Please try again."]
    advice = (
        "The AI analysis could not be completed due to a processing error. "
        "The health score above is estimated from rule-based analysis. "
        "Please retry or consult your healthcare provider for a full evaluation."
    )

    return {
        "patient_summary": (
            f"Rule-based analysis detected {len(abnormals)} potential abnormalities. "
            "Full AI analysis was unavailable — please retry."
        ),
        "health_score": score,
        "risk_level": risk,
        "abnormal_values": abnormal_values,
        "possible_conditions": conditions,
        "diet": ["Please consult a nutritionist for personalised advice."],
        "exercise": ["Please consult your doctor before starting any exercise programme."],
        "doctor_advice": advice,
    }
