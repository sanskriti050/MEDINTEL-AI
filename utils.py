"""
Medical-report PDF extraction.

Supports digital PDFs, scanned report pages, and photos saved as PDFs.  Extraction
uses embedded PDF text first, then local OCR when available, then Groq Vision for
image-only pages.  Each page is handled independently, so mixed PDFs work too.
"""

import base64
import io
import os
import re

import fitz  # PyMuPDF
from dotenv import load_dotenv

load_dotenv()


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def extract_text_from_pdf(uploaded_file) -> str:
    """Return readable text from a medical PDF, including scanned/photo PDF pages.

    The uploaded file is never written to disk.  For every page, the fastest and
    most accurate available source is selected: embedded text → local OCR →
    vision OCR.  This makes a report with a mix of digital and photographed pages
    usable in one upload.
    """
    try:
        uploaded_file.seek(0)
        raw_bytes = uploaded_file.read()
        if not raw_bytes:
            return ""

        pdf = fitz.open(stream=raw_bytes, filetype="pdf")
    except Exception as exc:
        print(f"[PDF] Unable to open file: {exc}")
        return ""

    try:
        pages = []
        for page_number, page in enumerate(pdf, start=1):
            # 1) Native PDF text (best for normal/generated PDFs)
            embedded = _extract_embedded_page_text(page)
            if _is_useful_page_text(embedded):
                pages.append(_page_block(page_number, embedded))
                continue

            # 2) Built-in Python OCR for image-only/scanned/photo PDFs.
            # This does not need a separately installed Tesseract application.
            image_bytes = _render_page_png(page)
            ocr_text = _try_rapidocr(image_bytes)
            if _is_useful_page_text(ocr_text):
                pages.append(_page_block(page_number, ocr_text))
                continue

            # 3) Tesseract remains an additional local OCR fallback when present.
            ocr_text = _try_tesseract_ocr(image_bytes)
            if _is_useful_page_text(ocr_text):
                pages.append(_page_block(page_number, ocr_text))
                continue

            # 4) Vision OCR is the final fallback for difficult photo pages.
            vision_text = _try_groq_vision_page(image_bytes, page_number)
            if _is_useful_page_text(vision_text):
                pages.append(_page_block(page_number, vision_text))
            else:
                print(f"[OCR] No readable text found on page {page_number}")

        return _clean("\n\n".join(pages))
    finally:
        pdf.close()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE TEXT + IMAGE HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _extract_embedded_page_text(page) -> str:
    """Read normal PDF text, including common column/block encodings."""
    try:
        text = page.get_text("text").strip()
        if text:
            return text

        blocks = page.get_text("blocks")
        text = "\n".join(
            block[4].strip() for block in blocks
            if len(block) > 4 and isinstance(block[4], str) and block[4].strip()
        )
        if text:
            return text

        raw = page.get_text("rawdict")
        words = []
        for block in raw.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    value = span.get("text", "").strip()
                    if value:
                        words.append(value)
        return " ".join(words)
    except Exception as exc:
        print(f"[PDF text] {exc}")
        return ""


def _render_page_png(page) -> bytes:
    """Render at OCR-friendly quality while keeping request payloads practical."""
    matrix = fitz.Matrix(2.5, 2.5)  # 180 DPI
    pixmap = page.get_pixmap(matrix=matrix, colorspace=fitz.csRGB, alpha=False)
    return pixmap.tobytes("png")


_RAPID_OCR = None


def _try_rapidocr(image_bytes: bytes) -> str:
    """OCR scanned/photo PDF pages without requiring the Tesseract desktop app."""
    global _RAPID_OCR
    try:
        from rapidocr_onnxruntime import RapidOCR

        if _RAPID_OCR is None:
            _RAPID_OCR = RapidOCR()
        result, _ = _RAPID_OCR(image_bytes)
        if not result:
            return ""
        # Each result row is [bounding_box, recognised_text, confidence].
        lines = [str(row[1]).strip() for row in result if len(row) >= 2 and str(row[1]).strip()]
        return "\n".join(lines)
    except Exception as exc:
        print(f"[Built-in OCR unavailable/failed] {exc}")
        return ""


def _try_tesseract_ocr(image_bytes: bytes) -> str:
    """Use local OCR when its optional executable is available."""
    try:
        import pytesseract
        from PIL import Image, ImageEnhance, ImageOps

        image = Image.open(io.BytesIO(image_bytes)).convert("L")
        image = ImageOps.autocontrast(image)
        image = ImageEnhance.Contrast(image).enhance(1.5)
        return pytesseract.image_to_string(image, config="--oem 3 --psm 6")
    except Exception as exc:
        # No local OCR is fine: Groq Vision below remains the automatic fallback.
        print(f"[Tesseract OCR unavailable/failed] {exc}")
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# VISION OCR FALLBACK
# ─────────────────────────────────────────────────────────────────────────────

def _try_groq_vision_page(image_bytes: bytes, page_number: int) -> str:
    """Transcribe an image-only report page using Groq Vision."""
    try:
        from groq import Groq

        api_key = os.getenv("GROQ_API_KEY", "")
        if not api_key:
            print("[Vision OCR] GROQ_API_KEY is not set")
            return ""

        encoded = base64.b64encode(image_bytes).decode("utf-8")
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Transcribe this medical-report page faithfully. Extract every "
                            "visible test name, result, unit, reference range, flag, date, "
                            "and clinical note. Preserve rows and values as clearly as possible. "
                            "Do not interpret, diagnose, summarise, or invent any data. "
                            "Return only the transcription."
                        ),
                    },
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded}"}},
                ],
            }],
            temperature=0,
            max_tokens=2500,
        )
        text = (response.choices[0].message.content or "").strip()
        if text:
            print(f"[Vision OCR] Page {page_number}: {len(text)} characters extracted")
        return text
    except Exception as exc:
        print(f"[Vision OCR] Page {page_number} failed: {exc}")
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _is_useful_page_text(text: str) -> bool:
    # A short lab slip can still be valid, so do not require the old 80 characters.
    return bool(text and len(text.strip()) >= 12)


def _page_block(page_number: int, text: str) -> str:
    return f"[Page {page_number}]\n{text.strip()}"


def _clean(text: str) -> str:
    text = re.sub(r"[ \t]{2,}", " ", text or "")
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
