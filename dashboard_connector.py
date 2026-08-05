"""
dashboard_connector.py
──────────────────────
Shared utility that converts an AI analysis result dict into a
dashboard report entry and saves it to session_state automatically.

Called from report.py after every successful analysis.
"""

import re
from datetime import date
from datetime import datetime
import streamlit as st


# ── Normal ranges for common lab tests ───────────────────────────────────────
_RANGES = {
    "hemoglobin":   (11.0, 17.0),
    "cholesterol":  (0.0,  200.0),
    "blood_sugar":  (70.0, 100.0),
    "tsh":          (0.4,  4.0),
    "creatinine":   (0.7,  1.2),
    "vitamin_d":    (20.0, 50.0),
}

# Regex patterns to pull numeric values from abnormal_values list
_PATTERNS = {
    "hemoglobin":  r"hemoglobin",
    "cholesterol": r"cholesterol",
    "blood_sugar": r"glucose|blood sugar|fasting|ppbs|rbs|fbs",
    "tsh":         r"\btsh\b",
    "creatinine":  r"creatinine",
    "vitamin_d":   r"vitamin\s*d",
}


def _extract_number(text: str) -> float | None:
    """Pull first float/int from a string like '11.2 g/dL (Low)'."""
    m = re.search(r"[\d]+\.?[\d]*", str(text))
    return float(m.group()) if m else None


def _find_vital_in_abnormals(abnormals: list, pattern: str) -> float | None:
    """Search abnormal_values list for a matching test and return its numeric result."""
    for item in abnormals:
        if not isinstance(item, dict):
            continue
        test_name = str(item.get("test", "")).lower()
        result    = str(item.get("result", ""))
        if re.search(pattern, test_name, re.IGNORECASE):
            return _extract_number(result)
    return None


def save_report_to_dashboard(ai_result: dict, report_type: str, filename: str = "") -> None:
    """
    Takes a completed AI analysis dict and appends a structured entry
    to st.session_state.dash_reports — no manual input needed.

    Also initialises dash_reports / dash_metrics if missing.
    """
    if "dash_reports" not in st.session_state:
        st.session_state.dash_reports = []

    score         = int(ai_result.get("health_score", 0))
    risk          = ai_result.get("risk_level", "Moderate")
    abnormals     = ai_result.get("abnormal_values", [])
    abnormal_count = len([a for a in abnormals if isinstance(a, dict) and a.get("test")])
    summary       = ai_result.get("patient_summary", "")

    # Build notes from first condition + advice snippet
    conditions    = [c for c in ai_result.get("possible_conditions", []) if c and str(c).strip()]
    advice        = ai_result.get("doctor_advice", "")
    notes_parts   = []
    if conditions:
        notes_parts.append(conditions[0][:60])
    if advice:
        notes_parts.append(advice[:60] + "…")
    notes = " | ".join(notes_parts) if notes_parts else filename or "—"

    # Extract key numeric vitals from abnormals (if present)
    vitals = {}
    for key, pattern in _PATTERNS.items():
        val = _find_vital_in_abnormals(abnormals, pattern)
        vitals[key] = val   # None if not found in abnormals

    entry = {
        "date":           str(date.today()),
        "report_type":    report_type,
        "score":          score,
        "risk":           risk,
        "abnormal_count": abnormal_count,
        "notes":          notes[:120],
        "source":         "auto",          # marks as auto-imported
        "filename":       filename or "uploaded",
        "added_at":       datetime.now().isoformat(),
        # vitals (may be None — dashboard filters these out)
        "hemoglobin":     vitals["hemoglobin"],
        "cholesterol":    vitals["cholesterol"],
        "blood_sugar":    vitals["blood_sugar"],
        "tsh":            vitals["tsh"],
        "creatinine":     vitals["creatinine"],
        "vitamin_d":      vitals["vitamin_d"],
    }

    # Avoid exact duplicates (same filename + same date)
    for existing in st.session_state.dash_reports:
        if (existing.get("filename") == entry["filename"] and
                existing.get("date") == entry["date"] and
                existing.get("score") == entry["score"]):
            return   # already saved

    st.session_state.dash_reports.append(entry)
