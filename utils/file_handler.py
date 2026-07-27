"""
File handling utility functions for reading and parsing document text.
"""
from typing import Any
import pdfplumber
from docx import Document


def read_text_file(uploaded_file: Any) -> str:
    """
    Read text from an uploaded file and decode it.
    Supports .txt, .pdf, and .docx files.
    """
    if not uploaded_file:
        return ""
    
    file_name = uploaded_file.name.lower()
    
    try:
        if file_name.endswith(".pdf"):
            return _read_pdf(uploaded_file)
        elif file_name.endswith(".docx"):
            return _read_docx(uploaded_file)
        else:
            return _read_text(uploaded_file)
    except Exception:
        return ""


def _read_text(uploaded_file: Any) -> str:
    """Read plain text file."""
    try:
        content = uploaded_file.getvalue()
        return content.decode("utf-8", errors="ignore")
    except Exception:
        try:
            uploaded_file.seek(0)
            return uploaded_file.read().decode("utf-8", errors="ignore")
        except Exception:
            return ""


def _read_pdf(uploaded_file: Any) -> str:
    """Extract text from PDF file."""
    text = ""
    try:
        uploaded_file.seek(0)
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        pass
    return text


def _read_docx(uploaded_file: Any) -> str:
    """Extract text from DOCX file."""
    text = ""
    try:
        uploaded_file.seek(0)
        doc = Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception:
        pass
    return text
