"""
UI component rendering the AI Suggestions tab.
Triggers OpenRouter completions to output granular optimization suggestions.
"""
import streamlit as st
from config.prompts import RESUME_ANALYSIS_PROMPT_TEMPLATE
from services.ai_service import ask_ai_stream

def render_ai_assistant(resume_text: str, job_text: str) -> None:
    """
    Render the AI Suggestions / Resume Assistant interface, streaming OpenRouter reports.
    """
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Resume Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="small-muted">Generate professional AI-powered resume feedback using OpenRouter.</div>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # State key to persist streaming output inside the current session
    if "ai_analysis_report" not in st.session_state:
        st.session_state.ai_analysis_report = ""

    # Button to trigger AI generation
    if st.button("Generate AI Suggestions"):
        with st.spinner("AI is analyzing the resume..."):
            try:
                # Truncate inputs to prevent OpenRouter token overflow
                short_resume = resume_text[:5000]
                short_job = job_text[:5000]

                # Format prompts
                prompt = RESUME_ANALYSIS_PROMPT_TEMPLATE.format(
                    resume_text=short_resume,
                    job_text=short_job
                )

                st.session_state.ai_analysis_report = "" # Clear previous report
                
                # Render inside chat message container for styling
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    streamed_text = ""

                    # Stream text chunk by chunk
                    for chunk in ask_ai_stream(prompt):
                        streamed_text += chunk
                        message_placeholder.markdown(
                            f'<div class="ai-stream-wrap">{streamed_text}</div>',
                            unsafe_allow_html=True
                        )
                    
                    st.session_state.ai_analysis_report = streamed_text

                st.success("AI Analysis Complete")
            except Exception as e:
                st.error(f"AI Error: {e}")
                
    elif st.session_state.ai_analysis_report:
        # If already analyzed, restore standard display block
        with st.chat_message("assistant"):
            st.markdown(
                f'<div class="ai-stream-wrap">{st.session_state.ai_analysis_report}</div>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)
