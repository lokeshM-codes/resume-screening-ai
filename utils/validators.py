"""
File and size validator utility functions.
"""
from typing import Any

def validate_file_size(uploaded_file: Any, max_mb: int) -> bool:
    """
    Validate that the uploaded file size does not exceed the max_mb limit.
    """
    if uploaded_file is None:
        return True
    try:
        size_bytes = uploaded_file.size
        size_mb = size_bytes / (1024 * 1024)
        return size_mb <= max_mb
    except AttributeError:
        try:
            uploaded_file.seek(0, 2)
            size = uploaded_file.tell()
            uploaded_file.seek(0)
            return (size / (1024 * 1024)) <= max_mb
        except Exception:
            return True
