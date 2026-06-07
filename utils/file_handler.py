"""
File handling utility functions for reading and parsing document text.
"""
from typing import Any

def read_text_file(uploaded_file: Any) -> str:
    """
    Read text from an uploaded file and decode it.
    """
    if not uploaded_file:
        return ""
    try:
        content = uploaded_file.getvalue()
        return content.decode("utf-8", errors="ignore")
    except Exception:
        try:
            uploaded_file.seek(0)
            return uploaded_file.read().decode("utf-8", errors="ignore")
        except Exception:
            return ""
