"""
UI component rendering the landing page headers, upload forms, and feature grids.
Handles size validations and updates analysis session state.
"""
import streamlit as st
from config.settings import MAX_UPLOAD_MB
from utils.validators import validate_file_size
from utils.file_handler import read_text_file
from services.resume_analyzer import analyze_resume

def render_upload_section() -> None:
    """
    Render the documents upload interface before analysis is run.
    """
    # Title / Hero Section
    st.markdown('<div class="ai-badge">AI-Powered Resume Analyzer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-title">Job <span class="gradient">Match</span> Analyzer</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sub-title">Upload your resume and job description and get an instant ATS compatibility score with AI-driven insights.</div>',
        unsafe_allow_html=True
    )

    with st.container(key="landing_card"):
        st.markdown(
            '<div class="upload-section-title">📎 Upload Documents</div>',
            unsafe_allow_html=True
        )

        col_a, col_b = st.columns([1, 1])

        with col_a:
            with st.container(key="resume_upload_card"):
                resume_file = st.file_uploader("📄 Upload Resume", type=["txt"])
                st.markdown(f'<span class="upload-note">⏺ Supports .txt files up to {MAX_UPLOAD_MB}MB</span>', unsafe_allow_html=True)

        with col_b:
            with st.container(key="job_upload_card"):
                job_file = st.file_uploader("📋 Upload Job Description", type=["txt"])
                st.markdown(f'<span class="upload-note">⏺ Supports .txt files up to {MAX_UPLOAD_MB}MB</span>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top: 1.75rem;"></div>', unsafe_allow_html=True)

        analyze_clicked = st.button("🔍 Analyze Match")

    # Feature Grid Details
    st.markdown(
        '<div class="feature-grid">'
        '<div class="feature-grid-item">'
        '<span class="icon">📊</span>'
        '<div class="label">ATS Score</div>'
        '<div class="desc">Get an instant ATS compatibility score</div>'
        '</div>'
        '<div class="feature-grid-item">'
        '<span class="icon">🧠</span>'
        '<div class="label">AI Suggestions</div>'
        '<div class="desc">Receive smart AI-powered resume feedback</div>'
        '</div>'
        '<div class="feature-grid-item">'
        '<span class="icon">🎯</span>'
        '<div class="label">Skill Gap Detection</div>'
        '<div class="desc">Identify missing keywords and technical skills</div>'
        '</div>'
        '<div class="feature-grid-item">'
        '<span class="icon">📈</span>'
        '<div class="label">Match Percentage</div>'
        '<div class="desc">Detailed job fit and compatibility breakdown</div>'
        '</div>'
        '<div class="feature-grid-item">'
        '<span class="icon">🚀</span>'
        '<div class="label">Resume Optimization</div>'
        '<div class="desc">Actionable tips to boost your resume score</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    if analyze_clicked:
        if resume_file and job_file:
            # Validate file sizes using configurable limit
            if not validate_file_size(resume_file, MAX_UPLOAD_MB):
                st.error(f"Resume file size exceeds the limit of {MAX_UPLOAD_MB}MB.")
                return
            if not validate_file_size(job_file, MAX_UPLOAD_MB):
                st.error(f"Job description file size exceeds the limit of {MAX_UPLOAD_MB}MB.")
                return

            # Read text content safely
            resume_text = read_text_file(resume_file)
            job_text = read_text_file(job_file)

            # Perform parsing and analysis
            with st.spinner("Analyzing your documents..."):
                result = analyze_resume(resume_text, job_text)

            # Store in session state
            st.session_state.resume_text = resume_text
            st.session_state.job_text = job_text
            st.session_state.result = result
            st.session_state.analyzed = True
            st.rerun()
        else:
            st.error("Please upload both files.")
