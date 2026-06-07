"""
UI component for the interactive Chatbot tab.
Allows the candidate to ask follow-up questions about their resume against the job description.
"""
import streamlit as st
from config.prompts import CHATBOT_SYSTEM_PROMPT
from services.ai_service import ask_ai_stream

def render_chatbot(resume_text: str, job_text: str) -> None:
    """
    Render an interactive chat widget inside the Chatbot tab.
    """
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 Resume Chatbot</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="small-muted">Ask questions about your resume alignment, skill gaps, or interview strategies.</div>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Clear chat history button
    if st.button("Clear Chat History", key="clear_chat_history"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Render previous messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User chat input
    user_input = st.chat_input("Type your question here (e.g. 'How can I highlight my Python experience better?')")

    if user_input:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Generate chatbot response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            streamed_text = ""

            # Inject document contexts in user message prompt
            contextual_prompt = f"""
Here is the context for my question:

RESUME CONTEXT (First 5000 characters):
{resume_text[:5000]}

JOB DESCRIPTION CONTEXT (First 5000 characters):
{job_text[:5000]}

---
USER QUESTION:
{user_input}
"""
            try:
                # Use OpenRouter completion with chatbot system instruction
                for chunk in ask_ai_stream(contextual_prompt, system_instruction=CHATBOT_SYSTEM_PROMPT):
                    streamed_text += chunk
                    message_placeholder.markdown(streamed_text)
                
                st.session_state.chat_history.append({"role": "assistant", "content": streamed_text})
            except Exception as e:
                st.error(f"Chatbot Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
