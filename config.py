"""
config.py
─────────
Central place to load secrets.
Works both locally (via .env) and on Streamlit Cloud (via st.secrets).
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_groq_api_key() -> str:
    """
    Returns the Groq API key.
    Priority:
      1. st.secrets (Streamlit Cloud deployment)
      2. os.getenv (local .env file)
    """
    # Try Streamlit secrets first (works on deployed app)
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
        if key:
            return key
    except Exception:
        pass

    # Fall back to environment variable / .env file
    key = os.getenv("GROQ_API_KEY", "")
    return key
