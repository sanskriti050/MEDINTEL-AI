import re

def calculate_health_score(report_text: str):

    score = 100
    abnormalities = []

    text = report_text.lower()

    rules = [
        ("hemoglobin", ["low", "decreased"], 8),
        ("wbc", ["high", "elevated"], 7),
        ("platelet", ["low"], 6),
        ("cholesterol", ["high"], 10),
        ("glucose", ["high"], 10),
        ("creatinine", ["high"], 12),
        ("bilirubin", ["high"], 10),
        ("tsh", ["high", "low"], 8)
    ]

    for test, keywords, penalty in rules:

        if test in text:

            for word in keywords:

                pattern = rf"{test}.*?{word}"

                if re.search(pattern, text):

                    score -= penalty
                    abnormalities.append(f"{test.title()} → {word.title()}")

    score = max(0, min(score, 100))

    if score >= 85:
        risk = "🟢 Low"

    elif score >= 65:
        risk = "🟡 Moderate"

    else:
        risk = "🔴 High"

    return score, risk, abnormalities