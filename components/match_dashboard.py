"""
UI component to render the dashboard header, match score ring, metrics, and progress bars.
"""
import streamlit as st
from config.constants import COLOR_SKILLS, COLOR_SOFT_SKILLS, COLOR_EXPERIENCE, COLOR_EDUCATION, COLOR_TEXT_KEYWORDS
from utils.helpers import score_color, score_label
from components.reusable_ui import render_bar

def render_match_dashboard(result: dict) -> None:
    """
    Render the main match dashboard dashboard interface with score ring and itemized breakdown.
    """
    final_score = max(0.0, min(100.0, result["final_score"] * 100.0))
    skills_score = max(0.0, min(100.0, result["skill_score"] * 100.0))
    soft_score = max(0.0, min(100.0, result["soft_skill_score"] * 100.0))
    experience_score = max(0.0, min(100.0, result["experience_score"] * 100.0))
    education_score = max(0.0, min(100.0, result["education_score"] * 100.0))
    text_score = max(0.0, min(100.0, result["text_score"] * 100.0))

    # Determine status details
    status_title = score_label(final_score)
    status_text = "The candidate has relevant skills and aligns with many job requirements."
    if final_score < 40:
        status_text = "The resume needs stronger alignment with the job description."
    elif final_score < 60:
        status_text = "The candidate matches some requirements, but several keywords are missing."
    elif final_score < 80:
        status_text = "The resume is a solid starting point with a few gaps to fix."

    ring_color = score_color(final_score)
    ring_bg = f"conic-gradient({ring_color} 0% {final_score:.1f}%, #e5e7eb {final_score:.1f}% 100%)"
    
    total_missing = (
        len(result["missing_skills"]) + 
        len(result["missing_soft_skills"]) + 
        len(result["missing_experience"]) + 
        len(result["missing_education"])
    )

    # -----------------------------------
    # TOP CARD
    # -----------------------------------
    st.markdown('<div class="top-card">', unsafe_allow_html=True)

    top_left, top_right = st.columns([0.55, 1.45])

    with top_left:
        st.markdown(
            f"""
            <div class="match-ring-wrap">
                <div class="match-ring" style="background:{ring_bg};">
                    <div class="match-ring-inner">
                        <div class="match-number">{final_score:.0f}</div>
                        <div class="match-label">MATCH</div>
                    </div>
                </div>
                <div class="match-badge" style="background:{ring_color};">
                    {status_title}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with top_right:
        st.markdown(
            f'<div class="summary-title">{status_title} — {total_missing} missing items found</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="summary-text">{status_text} The resume shows a match score of {final_score:.1f}%, with technical, soft-skill, experience, and education analysis separated for clarity.</div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="small-muted">✅ {len(result["matched_skills"])} technical matches</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="small-muted">✅ {len(result["matched_soft_skills"])} soft-skill matches</div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="small-muted">✅ {len(result["matched_experience"])} experience matches</div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="small-muted">✅ {len(result["matched_education"])} education matches</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------------
    # MATCH BREAKDOWN
    # -----------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Match Breakdown</div>', unsafe_allow_html=True)

    render_bar("Skills",          skills_score,     COLOR_SKILLS, has_data=bool(result["job_skills"]))
    render_bar("Soft Skills",     soft_score,       COLOR_SOFT_SKILLS, has_data=bool(result["job_soft_skills"]))
    render_bar("Experience",      experience_score, COLOR_EXPERIENCE, has_data=bool(result["job_experience"]))
    render_bar("Education",       education_score,  COLOR_EDUCATION, has_data=bool(result["job_education"]))
    render_bar("Text / Keywords", text_score,       COLOR_TEXT_KEYWORDS)
