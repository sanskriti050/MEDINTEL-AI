"""
health_engine.py
────────────────
Rule-based health scoring engine for MedIntel AI.

Used as a secondary validation layer alongside the Groq LLM score.
When the AI score is unavailable (API error / fallback), this engine
computes a score directly from the report text so the user always
gets a result.

It also provides a quick cross-check: if the rule-based score differs
greatly from the AI score, the analyzer blends both for a more
reliable final score.
"""

import re


# ── Scoring rules: (keyword, bad_signal_words, score_penalty) ────────────────
_RULES = [
    # Blood / CBC
    ("hemoglobin",   ["low", "decreased", "deficient"],  8),
    ("wbc",          ["high", "elevated", "increased"],  7),
    ("wbc",          ["low", "decreased"],               6),
    ("platelet",     ["low", "decreased", "reduced"],    8),
    ("platelet",     ["high", "elevated"],               4),
    ("rbc",          ["low", "decreased"],               5),
    ("mcv",          ["low", "microcytic"],               5),
    ("mcv",          ["high", "macrocytic"],              5),
    # Lipid / Cholesterol
    ("cholesterol",  ["high", "elevated", "borderline"], 10),
    ("ldl",          ["high", "elevated"],               10),
    ("hdl",          ["low", "decreased"],                8),
    ("triglyceride", ["high", "elevated", "increased"],   8),
    # Diabetes
    ("glucose",      ["high", "elevated", "diabetes"],   10),
    ("hba1c",        ["high", "elevated", "diabetic"],   12),
    ("fasting",      ["high", "elevated", "impaired"],    8),
    # Thyroid
    ("tsh",          ["high", "elevated"],                8),
    ("tsh",          ["low", "decreased", "suppressed"], 8),
    # Kidney
    ("creatinine",   ["high", "elevated", "increased"],  12),
    ("bun",          ["high", "elevated"],               10),
    ("egfr",         ["low", "decreased", "reduced"],    12),
    ("uric acid",    ["high", "elevated", "gout"],        7),
    # Liver
    ("bilirubin",    ["high", "elevated"],               10),
    ("alt",          ["high", "elevated"],                9),
    ("sgpt",         ["high", "elevated"],                9),
    ("ast",          ["high", "elevated"],                9),
    ("sgot",         ["high", "elevated"],                9),
    ("alp",          ["high", "elevated"],                6),
    ("albumin",      ["low", "decreased"],                8),
    # Vitamins
    ("vitamin d",    ["low", "deficient", "insufficient"], 5),
    ("vitamin b12",  ["low", "deficient"],                5),
    ("iron",         ["low", "deficient", "decreased"],   5),
    # Cardiac / BP
    ("troponin",     ["high", "elevated", "positive"],   15),
    ("blood pressure", ["high", "hypertension"],          8),
    # Inflammation
    ("crp",          ["high", "elevated"],                7),
    ("esr",          ["high", "elevated"],                5),
]


def calculate_health_score(report_text: str) -> tuple[int, str, list[str]]:
    """
    Analyse report text with keyword rules and return:
      (health_score: int 0–100,
       risk_level: str  'Low' | 'Moderate' | 'High',
       abnormalities: list[str])

    Parameters
    ----------
    report_text : str
        Raw text extracted from the medical report PDF.

    Returns
    -------
    tuple[int, str, list[str]]
        (score, risk, list_of_detected_abnormalities)
    """
    score = 100
    abnormalities: list[str] = []
    text = report_text.lower()

    for test, bad_signals, penalty in _RULES:
        if test not in text:
            continue
        for signal in bad_signals:
            # Look for the test keyword within ~80 chars of the bad signal word
            pattern = rf"{re.escape(test)}.{{0,80}}{re.escape(signal)}"
            if re.search(pattern, text):
                score -= penalty
                label = f"{test.title()} → {signal.title()}"
                if label not in abnormalities:
                    abnormalities.append(label)
                break   # one penalty per test per rule row

    # Clamp to valid range
    score = max(0, min(100, score))

    if score >= 75:
        risk = "Low"
    elif score >= 50:
        risk = "Moderate"
    else:
        risk = "High"

    return score, risk, abnormalities


def blend_scores(ai_score: int, rule_score: int, weight_ai: float = 0.75) -> int:
    """
    Blend AI score and rule-based score into a single final score.

    The AI score is weighted more heavily (default 75 %) because it
    understands context.  The rule engine acts as a sanity check.

    Parameters
    ----------
    ai_score    : int   Score from Groq LLM (0–100)
    rule_score  : int   Score from calculate_health_score (0–100)
    weight_ai   : float Weight given to AI score (0.0–1.0)

    Returns
    -------
    int  Blended score clamped to 0–100
    """
    blended = round(weight_ai * ai_score + (1.0 - weight_ai) * rule_score)
    return max(0, min(100, blended))
