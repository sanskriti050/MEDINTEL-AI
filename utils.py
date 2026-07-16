"""
utils.py — PDF text extraction with 3-strategy cascade:

  Strategy 1 → PyMuPDF  direct text  (fast, works on text-based PDFs)
  Strategy 2 → pdfplumber             (table-heavy lab reports)
  Strategy 3 → Groq Vision AI         (scanned / image PDFs — no Tesseract needed)
"""

import fitz          # PyMuPDF
import io
import re
import os
import base64

from dotenv import load_dotenv
load_dotenv()


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from ANY PDF:
    - Text-based PDFs  → PyMuPDF / pdfplumber
    - Scanned PDFs     → Groq LLaMA-4 Vision (image understanding, no Tesseract)
    Returns the extracted string, empty string if everything fails.
    """
    uploaded_file.seek(0)
    raw_bytes = uploaded_file.read()

    # ── Strategy 1: PyMuPDF ──────────────────────────────────────────────────
    text = _try_pymupdf(raw_bytes)
    if _is_good(text):
        return _clean(text)

    # ── Strategy 2: pdfplumber ───────────────────────────────────────────────
    text = _try_pdfplumber(raw_bytes)
    if _is_good(text):
        return _clean(text)

    # ── Strategy 3: Groq Vision AI (scanned PDF) ─────────────────────────────
    text = _try_groq_vision(raw_bytes)
    if _is_good(text):
        return _clean(text)

    # Nothing worked
    return ""


# ─────────────────────────────────────────────────────────────────────────────
# STRATEGY 1 — PyMuPDF
# ─────────────────────────────────────────────────────────────────────────────

def _try_pymupdf(raw_bytes: bytes) -> str:
    try:
        pdf   = fitz.open(stream=raw_bytes, filetype="pdf")
        parts = []

        for page in pdf:
            page_text = ""

            # 1a. Standard text
            t = page.get_text("text")
            if t and t.strip():
                page_text = t

            # 1b. Blocks (handles columnar/rotated text)
            if not page_text.strip():
                try:
                    blocks    = page.get_text("blocks")
                    page_text = "\n".join(
                        b[4] for b in blocks
                        if isinstance(b[4], str) and b[4].strip()
                    )
                except Exception:
                    pass

            # 1c. rawdict walk (unusual encodings)
            if not page_text.strip():
                try:
                    raw   = page.get_text("rawdict")
                    words = []
                    for block in raw.get("blocks", []):
                        for line in block.get("lines", []):
                            for span in line.get("spans", []):
                                w = span.get("text", "").strip()
                                if w:
                                    words.append(w)
                    page_text = " ".join(words)
                except Exception:
                    pass

            if page_text.strip():
                parts.append(page_text.strip())

        pdf.close()
        return "\n\n".join(parts)

    except Exception as e:
        print(f"[PyMuPDF] {e}")
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# STRATEGY 2 — pdfplumber
# ─────────────────────────────────────────────────────────────────────────────

def _try_pdfplumber(raw_bytes: bytes) -> str:
    try:
        import pdfplumber

        parts = []
        with pdfplumber.open(io.BytesIO(raw_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t and t.strip():
                    parts.append(t.strip())
                    continue

                # Table extraction for grid-format reports
                try:
                    for table in page.extract_tables():
                        for row in table:
                            row_text = "  |  ".join(
                                str(cell).strip() for cell in row if cell
                            )
                            if row_text.strip():
                                parts.append(row_text)
                except Exception:
                    pass

        return "\n\n".join(parts)

    except ImportError:
        return ""
    except Exception as e:
        print(f"[pdfplumber] {e}")
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# STRATEGY 3 — Groq LLaMA-4 Vision (scanned / image PDFs)
# ─────────────────────────────────────────────────────────────────────────────

def _try_groq_vision(raw_bytes: bytes) -> str:
    """
    Render each PDF page as a PNG image, send to Groq Vision AI,
    ask it to extract ALL text from the medical report image.
    Works on scanned PDFs, image-only PDFs, hand-typed reports — anything.
    """
    try:
        from groq import Groq
        from PIL import Image

        api_key = os.getenv("GROQ_API_KEY", "")
        if not api_key:
            print("[Vision] GROQ_API_KEY not set")
            return ""

        client = Groq(api_key=api_key)
        pdf    = fitz.open(stream=raw_bytes, filetype="pdf")
        parts  = []

        for page_num, page in enumerate(pdf):
            try:
                # Render page at 200 DPI as PNG
                mat = fitz.Matrix(200 / 72, 200 / 72)
                pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)

                img_bytes = pix.tobytes("png")

                # Encode to base64 for Groq Vision API
                b64_image = base64.b64encode(img_bytes).decode("utf-8")

                response = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": (
                                        "This is a scanned medical report / lab report image. "
                                        "Extract ALL text from this image exactly as it appears. "
                                        "Include every test name, value, unit, reference range, "
                                        "patient name, date, and any other text you can see. "
                                        "Output only the extracted text, nothing else."
                                    )
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{b64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=2000,
                    temperature=0
                )

                page_text = response.choices[0].message.content.strip()
                if page_text:
                    parts.append(f"[Page {page_num + 1}]\n{page_text}")
                    print(f"[Vision] Page {page_num + 1}: extracted {len(page_text)} chars")

            except Exception as page_err:
                print(f"[Vision] Page {page_num + 1} error: {page_err}")

        pdf.close()
        return "\n\n".join(parts)

    except Exception as e:
        print(f"[Vision] Fatal error: {e}")
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _is_good(text: str, min_chars: int = 80) -> bool:
    return bool(text) and len(text.strip()) >= min_chars


def _clean(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ─────────────────────────────────────────────────────────────────────────────
# REPORT TYPE DETECTION
# ─────────────────────────────────────────────────────────────────────────────

def detect_report_type(text: str) -> str:
    t = text.lower()

    if any(k in t for k in ["hemoglobin", "haemoglobin", "wbc", "rbc", "platelet",
                              "hematocrit", "haematocrit", "cbc", "complete blood count",
                              "neutrophil", "lymphocyte", "monocyte", "eosinophil",
                              "mcv", "mch", "mchc", "rdw", "packed cell"]):
        return "Blood / CBC Report"

    if any(k in t for k in ["glucose", "hba1c", "glycated hemoglobin", "fasting blood sugar",
                              "postprandial", "ppbs", "fbs", "rbs", "insulin", "diabetes",
                              "blood sugar", "glycosylated"]):
        return "Diabetes / Blood Sugar Report"

    if any(k in t for k in ["cholesterol", "ldl", "hdl", "triglyceride", "vldl",
                              "lipid profile", "non-hdl", "lipoprotein"]):
        return "Lipid / Cholesterol Report"

    if any(k in t for k in ["creatinine", "urea", "bun", "gfr", "egfr", "uric acid",
                              "kidney function", "renal function", "blood urea nitrogen"]):
        return "Kidney Function Test"

    if any(k in t for k in ["bilirubin", "sgpt", "sgot", "alt", "ast", "alp", "ggt",
                              "albumin", "liver function", "lft", "alkaline phosphatase"]):
        return "Liver Function Test"

    if any(k in t for k in ["tsh", "t3", "t4", "thyroid", "thyroxine",
                              "triiodothyronine", "free t3", "free t4", "ft3", "ft4"]):
        return "Thyroid Profile"

    if any(k in t for k in ["vitamin d", "vitamin b12", "calcium", "iron", "ferritin",
                              "folate", "folic acid", "zinc", "magnesium", "25-hydroxy"]):
        return "Vitamin & Mineral Profile"

    if any(k in t for k in ["urine", "urinalysis", "urine routine", "specific gravity",
                              "pus cells", "epithelial cells"]):
        return "Urine Analysis Report"

    if any(k in t for k in ["ecg", "ekg", "troponin", "cardiac", "echocardiogram",
                              "ejection fraction", "st segment"]):
        return "Cardiac Report"

    if any(k in t for k in ["x-ray", "xray", "mri", "ct scan", "ultrasound",
                              "sonography", "radiograph", "radiology", "impression"]):
        return "Radiology / Imaging Report"

    if any(k in t for k in ["testosterone", "estrogen", "progesterone", "fsh", "lh",
                              "prolactin", "cortisol", "dhea"]):
        return "Hormone Profile"

    if any(k in t for k in ["crp", "esr", "widal", "dengue", "malaria", "typhoid",
                              "hiv", "hepatitis", "antigen", "antibody", "covid", "pcr"]):
        return "Infection / Immunity Report"

    return "General Medical Report"
