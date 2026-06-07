"""
UI component for rendering the Technical and Soft Skills analysis tabs.
"""
import streamlit as st
from components.reusable_ui import render_tags

def render_skill_analysis(result: dict) -> None:
    """
    Render Technical Skills analysis content inside the tab container.
    """
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Technical Skills</div>', unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown("### Resume Skills")
        render_tags(result["resume_skills"], "tag-blue")

    with right:
        st.markdown("### Job Skills")
        render_tags(result["job_skills"], "tag-green")

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Matched Skills")
        render_tags(result["matched_skills"], "tag-green")
    with c2:
        st.markdown("### Missing Skills")
        if result["missing_skills"]:
            render_tags(result["missing_skills"], "tag-red")
        else:
            st.markdown('<span class="pill tag-green">No missing technical skills</span>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_soft_skill_analysis(result: dict) -> None:
    """
    Render Soft Skills analysis content inside the tab container.
    """
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Soft Skills</div>', unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown("### Resume Soft Skills")
        render_tags(result["resume_soft_skills"], "tag-blue")

    with right:
        st.markdown("### Job Soft Skills")
        render_tags(result["job_soft_skills"], "tag-green")

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Matched Soft Skills")
        render_tags(result["matched_soft_skills"], "tag-green")
    with c2:
        st.markdown("### Missing Soft Skills")
        if result["missing_soft_skills"]:
            render_tags(result["missing_soft_skills"], "tag-red")
        else:
            st.markdown('<span class="pill tag-green">No missing soft skills</span>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
