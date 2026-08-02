"""
RAG Engine — Retrieval-Augmented Generation for MedIntel AI
Lightweight TF-IDF similarity — no model download, no disk space needed.
Works instantly on first run.
"""

import re
from knowledge_base import MEDICAL_KNOWLEDGE


def _tokenize(text: str) -> list:
    return re.findall(r'\b[a-z]{3,}\b', text.lower())


def _tfidf_score(query_tokens: list, doc: str) -> float:
    """Simple TF-IDF cosine similarity between query tokens and document."""
    doc_tokens = _tokenize(doc)
    if not doc_tokens or not query_tokens:
        return 0.0
    doc_freq = {}
    for t in doc_tokens:
        doc_freq[t] = doc_freq.get(t, 0) + 1
    score = 0.0
    for t in set(query_tokens):
        if t in doc_freq:
            tf = doc_freq[t] / len(doc_tokens)
            score += tf
    return score


def retrieve_relevant_context(query: str, top_k: int = 5) -> str:
    """
    Retrieve most relevant medical knowledge chunks for the given query.
    Uses TF-IDF similarity — no internet or model download required.
    """
    try:
        query_tokens = _tokenize(query)
        if not query_tokens:
            return ""

        scored = []
        for chunk in MEDICAL_KNOWLEDGE:
            score = _tfidf_score(query_tokens, chunk)
            if score > 0:
                scored.append((score, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)
        top_chunks = [chunk for _, chunk in scored[:top_k]]

        if not top_chunks:
            return ""

        context = "\n".join(f"• {chunk}" for chunk in top_chunks)
        return f"\n\nRELEVANT MEDICAL KNOWLEDGE (use this to enrich your analysis):\n{context}\n"

    except Exception as e:
        print(f"[RAG] Retrieval failed: {e}")
        return ""


def get_rag_status() -> dict:
    """Return RAG system status for display."""
    return {
        "active": True,
        "chunks": len(MEDICAL_KNOWLEDGE),
        "model": "TF-IDF (no download)"
    }
