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

# AI Service Settings (OpenRouter API)
OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
DEFAULT_MODEL: str = "openai/gpt-oss-120b:free"
DEFAULT_TEMPERATURE: float = 0.5
DEFAULT_MAX_TOKENS_STREAM: int = 500
DEFAULT_MAX_TOKENS_STATIC: int = 700
