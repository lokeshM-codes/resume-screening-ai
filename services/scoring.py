"""
Scoring service logic for ATS resume analyzer.
Isolates calculations of component and final weights.
"""
from typing import List

def calculate_component_score(matched: List[str], job_items: List[str]) -> float:
    """
    Calculate keyword ratio score. Matches length logic in legacy back_end.py.
    """
    return len(matched) / len(job_items) if job_items else 0.0


def calculate_final_weighted_score(
    skill_score: float,
    soft_skill_score: float,
    experience_score: float,
    education_score: float,
    text_score: float
) -> float:
    """
    Calculate final weighted match score. Matches the exact formulas from legacy back_end.py.
    - Skills: 45%
    - Soft Skills: 20%
    - Experience: 20%
    - Education: 10%
    - Cosine Text similarity: 5%
    """
    return (
        0.45 * skill_score +
        0.20 * soft_skill_score +
        0.20 * experience_score +
        0.10 * education_score +
        0.05 * text_score
    )
