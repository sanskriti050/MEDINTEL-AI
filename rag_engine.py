"""
RAG Engine — Retrieval-Augmented Generation for MedIntel AI
Lightweight TF-IDF similarity — no model download, no disk space needed.
Works instantly on first run.

Two separate knowledge bases are indexed here because the domains don't
overlap:
  - MEDICAL_KNOWLEDGE (knowledge_base.py)  → lab test values / conditions,
    used by the Report Analyzer.
  - DRUG_KNOWLEDGE (drug_knowledge_base.py) → medicines / brand names,
    used by the Medicine Guide.
Each gets its own IDF table, built from its own corpus — mixing them into
one index would dilute both (a "high" that's common in lab results
shouldn't affect drug-name matching, and vice versa).
"""

import math
import re
from knowledge_base import MEDICAL_KNOWLEDGE
from drug_knowledge_base import DRUG_KNOWLEDGE


def _tokenize(text: str) -> list:
    return re.findall(r'\b[a-z]{3,}\b', text.lower())


def _build_idf(corpus: list) -> dict:
    """
    IDF(term) = log(total_docs / docs_containing_term) + 1 (smoothed).
    Rare/distinctive terms (e.g. "creatinine", "azithromycin") get a HIGH
    idf score. Common terms that appear in many chunks get a LOW score.
    """
    n_docs = len(corpus)
    doc_freq = {}
    for doc in corpus:
        seen = set(_tokenize(doc))
        for term in seen:
            doc_freq[term] = doc_freq.get(term, 0) + 1
    return {term: math.log((n_docs + 1) / (df + 1)) + 1 for term, df in doc_freq.items()}


def _tfidf_score(query_tokens: list, doc: str, idf_table: dict) -> float:
    doc_tokens = _tokenize(doc)
    if not doc_tokens or not query_tokens:
        return 0.0

    doc_term_count = {}
    for t in doc_tokens:
        doc_term_count[t] = doc_term_count.get(t, 0) + 1

    score = 0.0
    for t in set(query_tokens):
        if t in doc_term_count:
            tf = doc_term_count[t] / len(doc_tokens)
            idf = idf_table.get(t, 1.0)  # unseen terms get a neutral weight of 1.0
            score += tf * idf
    return score


# ── Lab-report knowledge base (Report Analyzer) ──────────────────────────────
_LAB_IDF = _build_idf(MEDICAL_KNOWLEDGE)


def retrieve_relevant_context(query: str, top_k: int = 5) -> str:
    """
    Retrieve most relevant LAB/CONDITION knowledge chunks for the given
    query (used by the Report Analyzer). Uses TF-IDF similarity.
    """
    try:
        query_tokens = _tokenize(query)
        if not query_tokens:
            return ""

        scored = [
            (_tfidf_score(query_tokens, chunk, _LAB_IDF), chunk)
            for chunk in MEDICAL_KNOWLEDGE
        ]
        scored = [(s, c) for s, c in scored if s > 0]
        scored.sort(key=lambda x: x[0], reverse=True)
        top_chunks = [chunk for _, chunk in scored[:top_k]]

        if not top_chunks:
            return ""

        context = "\n".join(f"• {chunk}" for chunk in top_chunks)
        return f"\n\nRELEVANT MEDICAL KNOWLEDGE (use this to enrich your analysis):\n{context}\n"

    except Exception as e:
        print(f"[RAG] Retrieval failed: {e}")
        return ""


# ── Drug knowledge base (Medicine Guide) ─────────────────────────────────────
def _drug_to_text(entry: dict) -> str:
    """Flatten a drug entry into a single string for tokenizing/matching."""
    return (
        f"{' '.join(entry['brand_names'])} {entry['generic_name']} "
        f"{entry['drug_class']} {entry['common_uses']} {entry['key_notes']}"
    )


_DRUG_TEXTS = [_drug_to_text(entry) for entry in DRUG_KNOWLEDGE]
_DRUG_IDF = _build_idf(_DRUG_TEXTS)


def retrieve_drug_context(query: str, top_k: int = 3) -> str:
    """
    Retrieve most relevant DRUG knowledge entries for the given medicine
    name query (used by the Medicine Guide). Matches against brand names,
    generic name, drug class, uses and key notes.
    """
    try:
        query_tokens = _tokenize(query)
        if not query_tokens:
            return ""

        scored = [
            (_tfidf_score(query_tokens, text, _DRUG_IDF), entry)
            for text, entry in zip(_DRUG_TEXTS, DRUG_KNOWLEDGE)
        ]
        scored = [(s, e) for s, e in scored if s > 0]
        scored.sort(key=lambda x: x[0], reverse=True)
        top_entries = [entry for _, entry in scored[:top_k]]

        if not top_entries:
            return ""

        blocks = []
        for e in top_entries:
            blocks.append(
                f"• Brand names: {', '.join(e['brand_names'])} | "
                f"Generic: {e['generic_name']} | Class: {e['drug_class']}\n"
                f"  Common uses: {e['common_uses']}\n"
                f"  Key notes: {e['key_notes']}"
            )
        context = "\n".join(blocks)
        return f"\n\nRELEVANT DRUG REFERENCE DATA (use this to ground your answer):\n{context}\n"

    except Exception as e:
        print(f"[RAG] Drug retrieval failed: {e}")
        return ""


def get_rag_status() -> dict:
    """Return RAG system status for display."""
    return {
        "active": True,
        "chunks": len(MEDICAL_KNOWLEDGE),
        "drug_chunks": len(DRUG_KNOWLEDGE),
        "model": "TF-IDF (no download)"
    }