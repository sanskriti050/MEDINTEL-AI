"""
RAG retriever for MedIntel AI.

Loads a pre-built FAISS index of embedded knowledge-base entries and
retrieves the top-k most relevant entries for a given query (patient
symptom description). This grounds the LLM's response in a curated
knowledge base instead of relying purely on the model's parametric
memory.

Run `python rag/build_index.py` once (or whenever knowledge_base.json
changes) to (re)build the index before using this retriever.
"""

import json
import os

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_KB_PATH = os.path.join(_BASE_DIR, "knowledge_base.json")
_INDEX_PATH = os.path.join(_BASE_DIR, "kb_index.faiss")
_META_PATH = os.path.join(_BASE_DIR, "kb_metadata.json")

_MODEL_NAME = "all-MiniLM-L6-v2"  # small, fast, free, runs locally


class RAGRetriever:
    """Singleton-style retriever: loads model + index once, reuses across calls."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        if not os.path.exists(_INDEX_PATH) or not os.path.exists(_META_PATH):
            raise FileNotFoundError(
                "FAISS index not found. Run `python rag/build_index.py` first "
                "to build the knowledge base index."
            )

        self.model = SentenceTransformer(_MODEL_NAME)
        self.index = faiss.read_index(_INDEX_PATH)

        with open(_META_PATH, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

    def retrieve(self, query: str, top_k: int = 3) -> list[dict]:
        """
        Return the top_k knowledge-base entries most relevant to `query`.
        Each result includes the original entry plus a similarity score.
        """
        query_vec = self.model.encode([query], normalize_embeddings=True)
        query_vec = np.asarray(query_vec, dtype="float32")

        scores, indices = self.index.search(query_vec, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            entry = dict(self.metadata[idx])
            entry["similarity_score"] = float(score)
            results.append(entry)

        return results

    def format_context(self, results: list[dict]) -> str:
        """Format retrieved entries into a context block for the LLM prompt."""
        if not results:
            return "No closely matching reference conditions found in knowledge base."

        blocks = []
        for r in results:
            blocks.append(
                f"- Reference condition: {r['condition']}\n"
                f"  Typical symptoms: {r['symptoms']}\n"
                f"  Description: {r['description']}\n"
                f"  Typical severity: {r['typical_severity']}\n"
                f"  Standard guidance: {r['standard_advice']}"
            )
        return "\n\n".join(blocks)
