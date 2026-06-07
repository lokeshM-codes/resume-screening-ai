"""
Constants for the AI Resume Analyzer UI and scoring.
"""
from typing import Dict

# Page Config Constants
PAGE_TITLE: str = "AI Resume Analyzer"
PAGE_ICON: str = "📄"
LAYOUT: str = "wide"

# Casing override maps for technical skills display
SPECIAL_SKILL_CASING: Dict[str, str] = {
    "sql": "SQL",
    "aws": "AWS",
    "ui": "UI",
    "ux": "UX",
    "nlp": "NLP",
    "ai": "AI",
    "ml": "ML",
    "api": "API",
    "rest api": "REST API",
    "node.js": "Node.js",
    "react": "React",
    "django": "Django",
    "flask": "Flask",
    "mongodb": "MongoDB",
    "mysql": "MySQL",
    "github": "GitHub",
}

# Score Range Labels & Descriptions
SCORE_CATEGORIES = {
    "strong": {
        "threshold": 80.0,
        "label": "Strong Match",
        "description": "The candidate has relevant skills and aligns with many job requirements.",
        "color": "#16A34A"
    },
    "good": {
        "threshold": 60.0,
        "label": "Good Match",
        "description": "The resume is a solid starting point with a few gaps to fix.",
        "color": "#EAB308"
    },
    "average": {
        "threshold": 40.0,
        "label": "Average Match",
        "description": "The candidate matches some requirements, but several keywords are missing.",
        "color": "#F97316"
    },
    "low": {
        "threshold": 0.0,
        "label": "Low Match",
        "description": "The resume needs stronger alignment with the job description.",
        "color": "#DC2626"
    }
}

# Sub-score colors
COLOR_SKILLS: str = "#E8A800"
COLOR_SOFT_SKILLS: str = "#2563EB"
COLOR_EXPERIENCE: str = "#E53935"
COLOR_EDUCATION: str = "#22C55E"
COLOR_TEXT_KEYWORDS: str = "#DC2626"
