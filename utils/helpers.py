"""
General utility helper functions for formatting and scores.
"""
from config.constants import SPECIAL_SKILL_CASING, SCORE_CATEGORIES

def pretty_skill(skill: str) -> str:
    """
    Format skill strings to their professional acronyms or standard capitalization.
    """
    skill = skill.strip()
    return SPECIAL_SKILL_CASING.get(skill.lower(), skill.title())


def score_label(score: float) -> str:
    """
    Get matching label (e.g. Strong Match, Good Match) based on final score.
    """
    for category_key, category in SCORE_CATEGORIES.items():
        if score >= category["threshold"]:
            return category["label"]
    return "Low Match"


def score_color(score: float) -> str:
    """
    Get matching color hex code based on final score.
    """
    for category_key, category in SCORE_CATEGORIES.items():
        if score >= category["threshold"]:
            return category["color"]
    return "#DC2626"
