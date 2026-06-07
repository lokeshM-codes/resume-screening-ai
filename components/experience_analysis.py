"""
UI component for rendering the Experience analysis tab.
"""
import streamlit as st
from components.reusable_ui import render_tags

def render_experience_analysis(result: dict) -> None:
    """
    Render Experience analysis content inside the tab container.
    """
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Experience</div>', unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown("### Resume Experience Terms")
        render_tags(result["resume_experience"], "tag-blue")

    with right:
        st.markdown("### Job Experience Terms")
        render_tags(result["job_experience"], "tag-green")

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Matched Experience Terms")
        render_tags(result["matched_experience"], "tag-green")
    with c2:
        st.markdown("### Missing Experience Terms")
        if result["missing_experience"]:
            render_tags(result["missing_experience"], "tag-red")
        else:
            st.markdown('<span class="pill tag-green">No missing experience terms</span>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
