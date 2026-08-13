"""
Build (or rebuild) the FAISS index for the RAG knowledge base.

Run this once after adding rag/knowledge_base.json, and again any time
you edit that file:

    python rag/build_index.py

It embeds each knowledge-base entry (condition + symptoms + description)
using a local sentence-transformer model and stores the vectors in a
FAISS index on disk, alongside the raw metadata for lookup at query time.
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

_MODEL_NAME = "all-MiniLM-L6-v2"


def build():
    with open(_KB_PATH, "r", encoding="utf-8") as f:
        kb = json.load(f)

    print(f"Loaded {len(kb)} knowledge base entries.")

    # Text used for embedding: condition name + symptoms is what we match
    # a patient's free-text symptom description against.
    texts = [f"{entry['condition']}. Symptoms: {entry['symptoms']}. {entry['description']}" for entry in kb]

    print(f"Loading embedding model '{_MODEL_NAME}' (first run downloads it)...")
    model = SentenceTransformer(_MODEL_NAME)

    print("Encoding knowledge base entries...")
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
    embeddings = np.asarray(embeddings, dtype="float32")

    dim = embeddings.shape[1]
    # Inner product on normalized vectors == cosine similarity
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    faiss.write_index(index, _INDEX_PATH)
    with open(_META_PATH, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)

    print(f"Saved FAISS index to {_INDEX_PATH}")
    print(f"Saved metadata to {_META_PATH}")
    print("Done. You can now use rag/retriever.py to query the knowledge base.")


if __name__ == "__main__":
    build()
