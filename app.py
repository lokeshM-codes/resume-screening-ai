"""
AI Resume Analyzer main application entry point.
"""
import streamlit as st

# Import configuration
from config.constants import PAGE_TITLE, PAGE_ICON, LAYOUT

# Import components
from components.reusable_ui import load_css
from components.upload_section import render_upload_section
from components.match_dashboard import render_match_dashboard
from components.skill_analysis import render_skill_analysis, render_soft_skill_analysis
from components.experience_analysis import render_experience_analysis
from components.education_analysis import render_education_analysis
from components.ai_assistant import render_ai_assistant
from components.chatbot import render_chatbot

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)

# Load central stylesheet
load_css("styles/main.css")

# -----------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if "result" not in st.session_state:
    st.session_state.result = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "job_text" not in st.session_state:
    st.session_state.job_text = ""


# -----------------------------------
# APPLICATION ROUTING / FLOW
# -----------------------------------
if not st.session_state.analyzed:
    # Render landing/upload section
    render_upload_section()
else:
    # Extract results and raw text from state
    result = st.session_state.result
    resume_text = st.session_state.resume_text
    job_text = st.session_state.job_text

    # Render dashboard header (Score ring & Breakdown bars)
    render_match_dashboard(result)

    # Render interactive details tabs
    tabs = st.tabs(["Skills", "Soft Skills", "Experience", "Education", "AI Features", "Chatbot"])

    with tabs[0]:
        render_skill_analysis(result)

    with tabs[1]:
        render_soft_skill_analysis(result)

    with tabs[2]:
        render_experience_analysis(result)

    with tabs[3]:
        render_education_analysis(result)

    with tabs[4]:
        render_ai_assistant(resume_text, job_text)

    with tabs[5]:
        render_chatbot(resume_text, job_text)

    # -----------------------------------
    # AI STATIC SUGGESTIONS (Dashboard footer)
    # -----------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Suggestions</div>', unsafe_allow_html=True)

    for suggestion in result["suggestions"]:
        st.markdown(
            f"""
            <div class="section-card" style="margin-bottom:12px; word-wrap:break-word; overflow-wrap:break-word;">
                {suggestion}
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------
    # RESET BUTTON
    # -----------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Analyze Another Resume"):
        st.session_state.analyzed = False
        st.session_state.result = None
        st.session_state.resume_text = ""
        st.session_state.job_text = ""
        if "chat_history" in st.session_state:
            st.session_state.chat_history = []
        if "ai_analysis_report" in st.session_state:
            st.session_state.ai_analysis_report = ""
        st.rerun()
