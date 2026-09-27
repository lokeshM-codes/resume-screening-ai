"""
Settings configuration for the AI Resume Analyzer.
Centralizes environment variables, upload limits, and API endpoints.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Upload limits
MAX_UPLOAD_MB: int = 20

def get_api_key() -> str:
    key = os.getenv("OPENROUTER_API_KEY", "")
    if key:
        return key
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "OPENROUTER_API_KEY" in st.secrets:
            return st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        pass
    return ""

# AI Service Settings (OpenRouter API)
OPENROUTER_API_KEY: str = get_api_key()
OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
DEFAULT_MODEL: str = "openai/gpt-oss-120b"
DEFAULT_TEMPERATURE: float = 0.4
DEFAULT_MAX_TOKENS_STREAM: int = 3500
DEFAULT_MAX_TOKENS_STATIC: int = 3000

