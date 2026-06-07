"""
UI component for rendering the Education analysis tab.
"""
import streamlit as st
from components.reusable_ui import render_tags

def render_education_analysis(result: dict) -> None:
    """
    Render Education analysis content inside the tab container.
    """
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Education</div>', unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown("### Resume Education Terms")
        render_tags(result["resume_education"], "tag-blue")

    with right:
        st.markdown("### Job Education Terms")
        render_tags(result["job_education"], "tag-green")

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Matched Education Terms")
        render_tags(result["matched_education"], "tag-green")
    with c2:
        st.markdown("### Missing Education Terms")
        if result["missing_education"]:
            render_tags(result["missing_education"], "tag-red")
        else:
            st.markdown('<span class="pill tag-green">No missing education terms</span>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
