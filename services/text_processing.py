"""
Text processing service for cleaning text and extracting keywords.
"""
import re
from typing import List

def clean_text(text: str) -> str:
    """
    Lowercase text, remove non-alphanumeric/spaces, and strip whitespace.
    Matches clean_text logic from legacy back_end.py.
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s\.\+#-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def phrase_present(text: str, phrase: str) -> bool:
    """
    Check if a word/phrase is present in the text bounded by word boundaries.
    Matches phrase_present logic from legacy back_end.py.
    """
    pattern = r"\b" + re.escape(phrase.lower()) + r"\b"
    return re.search(pattern, text.lower()) is not None


def extract_items(text: str, item_list: List[str]) -> List[str]:
    """
    Extract unique items from item_list present in text.
    Matches extract_items logic from legacy back_end.py.
    """
    found = []
    text = text.lower()

    for item in item_list:
        if phrase_present(text, item) and item not in found:
            found.append(item)

    return found
