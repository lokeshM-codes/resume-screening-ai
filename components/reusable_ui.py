"""
Reusable UI component widgets and helpers.
"""
import streamlit as st
from utils.helpers import pretty_skill

def load_css(css_file_path: str) -> None:
    """
    Read external CSS file and inject it into the Streamlit app using markdown.
    """
    try:
        with open(css_file_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading CSS file: {e}")


def render_tags(items: list, color_class: str = "tag-green") -> None:
    """
    Render a list of items as styled CSS pill tags.
    """
    if not items:
        st.write("No items found.")
        return

    html = []
    for item in items:
        html.append(
            f'<span class="pill {color_class}">{pretty_skill(item)}</span>'
        )
    st.markdown(" ".join(html), unsafe_allow_html=True)


def render_bar(title: str, value: float, color: str, has_data: bool = True) -> None:
    """
    Render a styled horizontal progress breakdown bar.
    """
    if not has_data:
        st.markdown(
            f"""
            <div class="bar-card">
                <div class="bar-head" style="margin-bottom:0;">
                    <span>{title}</span>
                    <span class="bar-no-jd">No job description</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    value_clamped = max(0.0, min(100.0, float(value)))
    st.markdown(
        f"""
        <div class="bar-card">
            <div class="bar-head">
                <span>{title}</span>
                <span>{value_clamped:.0f}%</span>
            </div>
            <div class="bar-track">
                <div class="bar-fill" style="width:{value_clamped}%; background:{color};"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
