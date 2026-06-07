"""
Main Resume Analyzer service orchestrator.
Composes text cleaning, vocabulary matching, cosine similarity, and scoring logic.
"""
from typing import Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data.technical_skills import TECHNICAL_SKILLS
from data.soft_skills import SOFT_SKILLS
from data.education_keywords import EDUCATION_TERMS, EXPERIENCE_TERMS
from services.text_processing import clean_text, extract_items
from services.scoring import calculate_component_score, calculate_final_weighted_score

def analyze_resume(resume_text: str, job_text: str) -> Dict[str, Any]:
    """
    Analyze resume content against a job description.
    Matches the exact analytical logic and output dictionary structure of legacy back_end.py.
    """
    resume_clean = clean_text(resume_text)
    job_clean = clean_text(job_text)

    # Calculate TF-IDF Cosine Similarity
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_clean, job_clean])
    text_score = cosine_similarity(vectors[0], vectors[1])[0][0]

    # Technical skills matching
    resume_skills = extract_items(resume_clean, TECHNICAL_SKILLS)
    job_skills = extract_items(job_clean, TECHNICAL_SKILLS)
    matched_skills = list(set(resume_skills) & set(job_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))

    # Soft skills matching
    resume_soft_skills = extract_items(resume_clean, SOFT_SKILLS)
    job_soft_skills = extract_items(job_clean, SOFT_SKILLS)
    matched_soft_skills = list(set(resume_soft_skills) & set(job_soft_skills))
    missing_soft_skills = list(set(job_soft_skills) - set(resume_soft_skills))

    # Experience matching
    resume_experience = extract_items(resume_clean, EXPERIENCE_TERMS)
    job_experience = extract_items(job_clean, EXPERIENCE_TERMS)
    matched_experience = list(set(resume_experience) & set(job_experience))
    missing_experience = list(set(job_experience) - set(resume_experience))

    # Education matching
    resume_education = extract_items(resume_clean, EDUCATION_TERMS)
    job_education = extract_items(job_clean, EDUCATION_TERMS)
    matched_education = list(set(resume_education) & set(job_education))
    missing_education = list(set(job_education) - set(resume_education))

    # Component ratio scores
    skill_score = calculate_component_score(matched_skills, job_skills)
    soft_skill_score = calculate_component_score(matched_soft_skills, job_soft_skills)
    experience_score = calculate_component_score(matched_experience, job_experience)
    education_score = calculate_component_score(matched_education, job_education)

    # Combined final score
    final_score = calculate_final_weighted_score(
        skill_score=skill_score,
        soft_skill_score=soft_skill_score,
        experience_score=experience_score,
        education_score=education_score,
        text_score=text_score
    )

    # Standard recommendations/suggestions
    suggestions: List[str] = []

    if missing_skills:
        suggestions.append("Add missing technical skills: " + ", ".join(missing_skills))

    if missing_soft_skills:
        suggestions.append("Add missing soft skills: " + ", ".join(missing_soft_skills))

    if missing_experience:
        suggestions.append("Improve experience section with: " + ", ".join(missing_experience))

    if missing_education:
        suggestions.append("Add education-related keywords: " + ", ".join(missing_education))

    if "project" not in resume_clean and "projects" not in resume_clean:
        suggestions.append("Add a projects section to strengthen your resume.")

    if "certification" not in resume_clean and "certifications" not in resume_clean:
        suggestions.append("Add certifications to improve selection chances.")

    if not suggestions:
        suggestions.append("Your resume is a strong match for this job role.")

    return {
        "final_score": final_score,
        "text_score": text_score,
        "skill_score": skill_score,
        "soft_skill_score": soft_skill_score,
        "experience_score": experience_score,
        "education_score": education_score,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_soft_skills": resume_soft_skills,
        "job_soft_skills": job_soft_skills,
        "matched_soft_skills": matched_soft_skills,
        "missing_soft_skills": missing_soft_skills,
        "resume_experience": resume_experience,
        "job_experience": job_experience,
        "matched_experience": matched_experience,
        "missing_experience": missing_experience,
        "resume_education": resume_education,
        "job_education": job_education,
        "matched_education": matched_education,
        "missing_education": missing_education,
        "suggestions": suggestions
    }
