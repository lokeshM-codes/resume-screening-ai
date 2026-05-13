import streamlit as st

from back_end import analyze_resume


# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# -----------------------------------
# HELPERS
# -----------------------------------
def pretty_skill(skill: str) -> str:
    skill = skill.strip()
    special = {
        "sql": "SQL",
        "aws": "AWS",
        "ui": "UI",
        "ux": "UX",
        "nlp": "NLP",
        "ai": "AI",
        "ml": "ML",
        "api": "API",
        "rest api": "REST API",
        "node.js": "Node.js",
        "react": "React",
        "django": "Django",
        "flask": "Flask",
        "mongodb": "MongoDB",
        "mysql": "MySQL",
        "github": "GitHub",
    }
    return special.get(skill.lower(), skill.title())


def score_label(score: float) -> str:
    if score >= 80:
        return "Strong Match"
    if score >= 60:
        return "Good Match"
    if score >= 40:
        return "Average Match"
    return "Low Match"


def score_color(score: float) -> str:
    if score >= 80:
        return "#16A34A"
    if score >= 60:
        return "#EAB308"
    if score >= 40:
        return "#F97316"
    return "#DC2626"


def render_tags(items, color_class="tag-green"):
    if not items:
        st.write("No items found.")
        return

    html = []
    for item in items:
        html.append(
            f'<span class="pill {color_class}">{pretty_skill(item)}</span>'
        )
    st.markdown(" ".join(html), unsafe_allow_html=True)


def render_bar(title: str, value: float, color: str, has_data: bool = True):
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

    value = max(0, min(100, float(value)))
    st.markdown(
        f"""
        <div class="bar-card">
            <div class="bar-head">
                <span>{title}</span>
                <span>{value:.0f}%</span>
            </div>
            <div class="bar-track">
                <div class="bar-fill" style="width:{value}%; background:{color};"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def reset_app():
    st.session_state.analyzed = False
    st.session_state.result = None
    st.session_state.resume_text = ""
    st.session_state.job_text = ""


# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown(
    """
<style>
    .stApp {
        background: #f5f7fb;
        color: #111827;
    }

    /* Fix invisible labels */
    label, .stMarkdown p, .stMarkdown span, .stFileUploader label {
        color: #111827 !important;
    }

    /* Ensure file uploader text is visible */
    .stFileUploader label {
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }

    .main-title {
        font-size: 2.4rem;
        font-weight: 900;
        color: #111827;
        line-height: 1.05;
        margin-bottom: 0.25rem;
        letter-spacing: -0.03em;
    }

    .sub-title {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 1rem;
    }

    .top-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.04);
    }

    .section-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.03);
    }

    .summary-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0.5rem;
    }

    .summary-text {
        color: #6b7280;
        font-size: 1rem;
        line-height: 1.7;
    }

    .match-ring {
        width: 190px;
        height: 190px;
        border-radius: 50%;
        padding: 11px;
        margin: 0 auto;
        box-shadow: 0 8px 28px rgba(0,0,0,0.08);
        background: conic-gradient(#16a34a 0%, #16a34a 0%, #e5e7eb 0%, #e5e7eb 100%);
    }

    .match-ring-inner {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: #ffffff;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 1px solid #eef2f7;
    }

    .match-number {
        font-size: 3rem;
        font-weight: 900;
        line-height: 1;
        color: #16a34a;
        margin-bottom: 0.25rem;
    }

    .match-label {
        font-size: 0.84rem;
        letter-spacing: 0.18em;
        color: #6b7280;
        font-weight: 800;
    }

    .match-badge {
        display: inline-block;
        margin-top: 12px;
        padding: 8px 14px;
        border-radius: 999px;
        color: white;
        font-weight: 700;
        font-size: 0.9rem;
    }

    .bar-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }

    .bar-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.95rem;
        font-weight: 800;
        color: #374151;
        margin-bottom: 10px;
    }

    .bar-track {
        width: 100%;
        height: 10px;
        border-radius: 999px;
        background: #eef2f7;
        overflow: hidden;
    }

    .bar-fill {
        height: 100%;
        border-radius: 999px;
    }

    /* Fix 1 – Always show section content, never hide on hover */
    .section-card,
    .section-card *,
    [data-testid="stTabsContent"] > div,
    [data-testid="stTabsContent"] > div * {
        visibility: visible !important;
        display: revert !important;
        opacity: 1 !important;
        pointer-events: auto !important;
    }
    
    /* Muted label for no-JD bars */
    .bar-no-jd {
        color: #9ca3af;
        font-size: 0.88rem;
        font-style: italic;
        font-weight: 600;
    }

    /* Ensure pill tags are always inline-block */
    .pill {
        display: inline-block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }


    .pill {
        display: inline-block;
        padding: 8px 14px;
        margin: 6px 8px 0 0;
        border-radius: 999px;
        font-size: 0.92rem;
        font-weight: 800;
        color: white;
        box-shadow: 0 8px 18px rgba(0,0,0,0.08);
    }

    .tag-green {
        background: linear-gradient(135deg, #16a34a, #22c55e);
    }

    .tag-red {
        background: linear-gradient(135deg, #dc2626, #ef4444);
    }

    .tag-blue {
        background: linear-gradient(135deg, #2563eb, #38bdf8);
    }

    .tag-gray {
        background: linear-gradient(135deg, #475569, #64748b);
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 900;
        color: #111827;
        margin-bottom: 0.8rem;
    }

    .feature-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 18px;
        min-height: 135px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.03);
    }

    .feature-name {
        font-size: 1.05rem;
        font-weight: 900;
        color: #111827;
        margin-bottom: 0.35rem;
    }

    .feature-desc {
        color: #6b7280;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .stButton > button {
        border: none;
        border-radius: 14px;
        padding: 0.9rem 1rem;
        font-size: 1rem;
        font-weight: 900;
        color: white;
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        box-shadow: 0 10px 20px rgba(17,24,39,0.12);
    }

    .stButton > button:hover {
        filter: brightness(1.05);
    }

    .upload-note {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.35rem;
    }

    .small-muted {
        color: #6b7280;
        font-size: 0.92rem;
    }
</style>
""",
    unsafe_allow_html=True
)


# -----------------------------------
# SESSION STATE
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
# TITLE
# -----------------------------------
st.markdown('<div class="main-title">Job Matcher</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Upload your resume and job description to see how well you match.</div>',
    unsafe_allow_html=True
)


# -----------------------------------
# BEFORE ANALYSIS
# -----------------------------------
if not st.session_state.analyzed:
    # Removed invalid HTML wrapping that caused empty white boxes
    c1, c2 = st.columns([1, 1])

    with c1:
        resume_file = st.file_uploader("Upload Resume", type=["txt"])
        st.markdown('<div class="upload-note">Use a plain text resume for now.</div>', unsafe_allow_html=True)

    with c2:
        job_file = st.file_uploader("Upload Job Description", type=["txt"])
        st.markdown('<div class="upload-note">Use a plain text job description for now.</div>', unsafe_allow_html=True)

    analyze_clicked = st.button("Analyze Match")

    if analyze_clicked:
        if resume_file and job_file:
            resume_text = resume_file.getvalue().decode("utf-8", errors="ignore")
            job_text = job_file.getvalue().decode("utf-8", errors="ignore")

            st.session_state.resume_text = resume_text
            st.session_state.job_text = job_text
            st.session_state.result = analyze_resume(resume_text, job_text)
            st.session_state.analyzed = True
            st.rerun()
        else:
            st.error("Please upload both files.")

    st.stop()


# -----------------------------------
# RESULT DATA
# -----------------------------------
result = st.session_state.result
resume_text = st.session_state.resume_text
job_text = st.session_state.job_text

final_score = max(0.0, min(100.0, result["final_score"] * 100.0))
skills_score = max(0.0, min(100.0, result["skill_score"] * 100.0))
soft_score = max(0.0, min(100.0, result["soft_skill_score"] * 100.0))
experience_score = max(0.0, min(100.0, result["experience_score"] * 100.0))
education_score = max(0.0, min(100.0, result["education_score"] * 100.0))
text_score = max(0.0, min(100.0, result["text_score"] * 100.0))

status_title = "Strong Match"
status_text = "The candidate has relevant skills and aligns with many job requirements."
if final_score < 40:
    status_title = "Low Match"
    status_text = "The resume needs stronger alignment with the job description."
elif final_score < 60:
    status_title = "Average Match"
    status_text = "The candidate matches some requirements, but several keywords are missing."
elif final_score < 80:
    status_title = "Good Match"
    status_text = "The resume is a solid starting point with a few gaps to fix."

ring_color = score_color(final_score)
ring_bg = f"conic-gradient({ring_color} 0% {final_score:.1f}%, #e5e7eb {final_score:.1f}% 100%)"


# -----------------------------------
# TOP CARD
# -----------------------------------
st.markdown('<div class="top-card">', unsafe_allow_html=True)

top_left, top_right = st.columns([0.55, 1.45])

with top_left:
    st.markdown(
        f"""
        <div class="match-ring" style="background:{ring_bg};">
            <div class="match-ring-inner">
                <div class="match-number">{final_score:.0f}</div>
                <div class="match-label">MATCH</div>
            </div>
        </div>
        <div style="text-align:center; margin-top:12px;">
            <span class="match-badge" style="background:{ring_color};">
                {status_title}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

with top_right:
    st.markdown(
        f'<div class="summary-title">{status_title} — {len(result["missing_skills"]) + len(result["missing_soft_skills"]) + len(result["missing_experience"]) + len(result["missing_education"])} missing items found</div>',
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

    if st.button("Fix Missing Keywords"):
        st.info("The AI Features section below is ready for future OpenRouter integration.")

st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------
# MATCH BREAKDOWN
# -----------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Match Breakdown</div>', unsafe_allow_html=True)

render_bar("Skills",        skills_score,     "#E8A800", has_data=bool(result["job_skills"]))
render_bar("Soft Skills",   soft_score,       "#2563EB", has_data=bool(result["job_soft_skills"]))
render_bar("Experience",    experience_score, "#E53935", has_data=bool(result["job_experience"]))
render_bar("Education",     education_score,  "#22C55E", has_data=bool(result["job_education"]))
render_bar("Text / Keywords", text_score,     "#DC2626")


# -----------------------------------
# TABS
# -----------------------------------
st.markdown("<br>", unsafe_allow_html=True)
tabs = st.tabs(["Skills", "Soft Skills", "Experience", "Education", "AI Features"])


# -----------------------------------
# SKILLS TAB
# -----------------------------------
with tabs[0]:
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


# -----------------------------------
# SOFT SKILLS TAB
# -----------------------------------
with tabs[1]:
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


# -----------------------------------
# EXPERIENCE TAB
# -----------------------------------
with tabs[2]:
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


# -----------------------------------
# EDUCATION TAB
# -----------------------------------
with tabs[3]:
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


# -----------------------------------
# AI FEATURES TAB
# -----------------------------------
with tabs[4]:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Features</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="small-muted">These features can be connected later with OpenRouter AI.</div>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    a3, a4 = st.columns(2)

    with a1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-name">Resume Enhancement</div>
                <div class="feature-desc">Rewrite the resume in ATS-friendly language with stronger keywords and a better professional summary.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with a2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-name">Interview Questions</div>
                <div class="feature-desc">Generate technical and HR interview questions from the job description and resume profile.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with a3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-name">Learning Suggestions</div>
                <div class="feature-desc">Show a learning roadmap based on the missing keywords and technologies required for the role.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with a4:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-name">ATS Optimization</div>
                <div class="feature-desc">Highlight missing sections, weak keywords, and formatting issues that may affect selection.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------
# AI SUGGESTIONS
# -----------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">AI Suggestions</div>', unsafe_allow_html=True)

for suggestion in result["suggestions"]:
    st.markdown(
        f"""
        <div class="section-card" style="margin-bottom:12px;">
            {suggestion}
        </div>
        """,
        unsafe_allow_html=True
    )


# -----------------------------------
# RESET
# -----------------------------------
st.markdown("<br>", unsafe_allow_html=True)
if st.button("Analyze Another Resume"):
    reset_app()
    st.rerun()