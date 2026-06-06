import streamlit as st
from ai_features import ask_ai, ask_ai_stream
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
    /* =========================================================
       GLOBAL / APP
       ========================================================= */
    .stApp {
        background: #f5f7fb;
        color: #111827;
    }

    /* Main block container – modern dashboard proportions */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 2.5rem;
        padding-left: clamp(1rem, 2.5vw, 2rem);
        padding-right: clamp(1rem, 2.5vw, 2rem);
        max-width: 1320px;
        margin-left: auto;
        margin-right: auto;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    .stApp > header {
        background: transparent;
    }

    /* Global word-wrap safety net for any text node */
    html, body, .stApp, p, span, li, h1, h2, h3, h4, h5, h6, label, div {
        word-wrap: break-word;
        overflow-wrap: break-word;
        -webkit-hyphens: auto;
        -ms-hyphens: auto;
        hyphens: auto;
    }

    /* =========================================================
       FILE UPLOADER  –  premium SaaS UX
       ========================================================= */
    /* Uploader label above dropzone */
    .stFileUploader label {
        color: #111827 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        line-height: 1.4 !important;
        margin-bottom: 8px !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
        visibility: visible !important;
        opacity: 1 !important;
        height: auto !important;
        min-height: unset !important;
        padding: 0 !important;
        pointer-events: none !important;
    }

    /* Dropzone – premium glass card style */
    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        background: #fafbfc !important;
        border: 2px dashed #d1d5db !important;
        border-radius: 16px !important;
        padding: 28px 20px !important;
        min-height: 120px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
        cursor: pointer !important;
        position: relative;
        overflow: hidden;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"]::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(37,99,235,0.04), rgba(99,102,241,0.04));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"]:hover::before {
        opacity: 1;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #2563eb !important;
        background: #f0f5ff !important;
        box-shadow: 0 4px 20px rgba(37,99,235,0.08) !important;
        transform: translateY(-1px);
    }

    /* Dropzone text content */
    .stFileUploader [data-testid="stFileUploaderDropzone"] * {
        color: #111827 !important;
        visibility: visible !important;
        opacity: 1 !important;
        text-align: center !important;
        position: relative;
        z-index: 1;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] small {
        font-size: 0.85rem !important;
        color: #9ca3af !important;
        margin-top: 4px;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] span {
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }

    /* Upload icon inside dropzone */
    .stFileUploader [data-testid="stFileUploaderDropzone"] svg {
        width: 32px !important;
        height: 32px !important;
        color: #2563eb !important;
        opacity: 0.6 !important;
        margin-bottom: 6px;
    }

    /* ---- Uploaded file info (file name + size) ---- */
    /* ---- Uploaded file info (file name + size) ---- */
    .stFileUploader [data-testid="stFileChips"] {
        margin-top: 12px !important;
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important;
    }

    /* Target the file container chip */
    .stFileUploader [data-testid="stFileChip"] {
        background: #f0fdf4 !important; /* light green background */
        border: 1px solid #bbf7d0 !important; /* light green border */
        border-radius: 12px !important;
        padding: 10px 14px !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        width: 100% !important;
        min-width: 0 !important; /* Prevent text overflow clipping */
        box-sizing: border-box !important;
        box-shadow: 0 4px 12px rgba(22, 163, 74, 0.04) !important;
        transition: all 0.2s ease !important;
        position: relative !important;
        overflow: visible !important; /* Ensure nothing inside is clipped */
    }

    .stFileUploader [data-testid="stFileChip"]:hover {
        box-shadow: 0 6px 16px rgba(22, 163, 74, 0.08) !important;
        border-color: #86efac !important;
    }

    /* Text inside the file chip */
    .stFileUploader [data-testid="stFileChip"] * {
        color: #166534 !important; /* deep green text */
        font-weight: 500 !important;
    }

    /* Custom success check icon before the file chip content */
    .stFileUploader [data-testid="stFileChip"]::before {
        content: '✓';
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 20px !important;
        height: 20px !important;
        border-radius: 50% !important;
        background: #16a34a !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 0.8rem !important;
        flex-shrink: 0 !important;
        box-shadow: 0 2px 6px rgba(22, 163, 74, 0.2) !important;
        animation: scaleIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }

    /* Hide the default document icon and preview containers to replace it with our checkmark */
    .stFileUploader [data-testid="stFileChip"] svg {
        display: none !important;
    }
    .stFileUploader [data-testid="stFileChipImagePreview"] {
        display: none !important;
    }

    /* Ensure file name is fully visible and wraps correctly */
    .stFileUploader [data-testid="stFileChipName"] {
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        word-break: break-all !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        display: block !important;
        margin-right: auto !important;
        color: #166534 !important;
    }

    /* Custom success text indicator next to name */
    .stFileUploader [data-testid="stFileChipName"]::after {
        content: " • uploaded successfully";
        display: inline !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        color: #15803d !important;
        opacity: 0.95 !important;
    }

    /* Force delete icon SVG to remain visible */
    .stFileUploader [data-testid="stFileChip"] [data-testid="stFileChipDeleteBtn"] svg {
        display: inline-block !important;
    }

    /* Remove file button styling */
    .stFileUploader [data-testid="stFileChipDeleteBtn"] {
        color: #b91c1c !important;
        background: transparent !important;
        border: none !important;
        padding: 4px 8px !important;
        border-radius: 8px !important;
        transition: all 0.2s !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .stFileUploader [data-testid="stFileChipDeleteBtn"]:hover {
        background: rgba(239, 68, 68, 0.1) !important;
        color: #ef4444 !important;
    }

    /* Force the dropzone child list container to expand fully */
    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        align-items: stretch !important;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] > div {
        width: 100% !important;
    }

    /* Style the upload button inside the dropzone */
    .stFileUploader [data-testid="stFileUploaderDropzone"] button,
    .stFileUploader [data-testid="stFileUploaderDropzone"] [data-testid="baseButton-secondary"] {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15) !important;
        transition: all 0.2s ease !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        height: auto !important;
        margin: 0 auto !important;
    }

    .stFileUploader [data-testid="stFileUploaderDropzone"] button:hover,
    .stFileUploader [data-testid="stFileUploaderDropzone"] [data-testid="baseButton-secondary"]:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.25) !important;
        transform: translateY(-1px) !important;
    }

    .stFileUploader [data-testid="stFileUploaderDropzone"] button *,
    .stFileUploader [data-testid="stFileUploaderDropzone"] [data-testid="baseButton-secondary"] * {
        color: white !important;
    }

    /* Style the progress/loading bar with animation */
    .stFileUploader [data-testid="stFileUploader"] div[role="progressbar"] {
        height: 6px !important;
        border-radius: 999px !important;
        background-color: #f3f4f6 !important;
        overflow: hidden !important;
        margin-top: 8px !important;
    }
    .stFileUploader [data-testid="stFileUploader"] div[role="progressbar"] > div {
        background: linear-gradient(90deg, #10b981, #34d399, #10b981) !important;
        background-size: 200% 100% !important;
        border-radius: 999px !important;
        animation: progressShimmer 1.5s infinite linear !important;
    }

    @keyframes progressShimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    @keyframes scaleIn {
        0% { transform: scale(0.8); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }

    /* Upload note below dropzone */
    .upload-note {
        display: flex !important;
        align-items: center !important;
        gap: 4px !important;
        color: #9ca3af !important;
        font-size: 0.83rem !important;
        margin-top: 8px !important;
        line-height: 1.4 !important;
    }

    /* Animation keyframes */
    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(-4px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* =========================================================
       LANDING HERO
       ========================================================= */
    .ai-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #eef2ff, #e0e7ff);
        border: 1px solid #c7d2fe;
        border-radius: 999px;
        padding: 6px 14px 6px 10px;
        font-size: 0.8rem;
        font-weight: 700;
        color: #4338ca;
        letter-spacing: 0.02em;
        margin-bottom: 1.2rem;
    }
    .ai-badge::before {
        content: '✦';
        font-size: 0.9rem;
    }

    .main-title {
        font-size: clamp(1.8rem, 4vw, 2.6rem);
        font-weight: 900;
        color: #111827;
        line-height: 1.15;
        margin-bottom: 0.4rem;
        margin-top: 0.3rem;
        letter-spacing: -0.03em;
        word-wrap: break-word;
    }
    .main-title .gradient {
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .sub-title {
        font-size: clamp(0.95rem, 1.6vw, 1.05rem);
        color: #6b7280;
        margin-bottom: 2rem;
        line-height: 1.55;
        max-width: 640px;
    }

    /* =========================================================
       LANDING PAGE CARD  –  upload section
       ========================================================= */
    /* =========================================================
       LANDING PAGE CARD  –  upload section
       ========================================================= */
    .st-key-landing_card {
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 24px !important;
        padding: clamp(28px, 4vw, 44px) !important;
        box-shadow: 0 8px 30px rgba(0,0,0,0.04) !important;
        text-align: center !important;
        margin-top: 0.5rem !important;
        transition: box-shadow 0.3s ease !important;
    }
    .st-key-landing_card:hover {
        box-shadow: 0 12px 40px rgba(0,0,0,0.07) !important;
    }
    .st-key-landing_card .stFileUploader {
        text-align: left !important;
    }
    .st-key-landing_card .upload-section-title {
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        color: #111827 !important;
        margin-bottom: 1.5rem !important;
        text-align: left !important;
    }

    /* Upload card container */
    .st-key-resume_upload_card, .st-key-job_upload_card {
        background: #ffffff !important;
        border: 1px solid #f3f4f6 !important;
        border-radius: 16px !important;
        padding: 18px 20px 20px !important;
        transition: box-shadow 0.25s ease, transform 0.25s ease !important;
    }
    .st-key-resume_upload_card:hover, .st-key-job_upload_card:hover {
        box-shadow: 0 8px 28px rgba(0,0,0,0.06) !important;
        transform: translateY(-2px) !important;
    }

    /* =========================================================
       LANDING FEATURES
       ========================================================= */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
    }
    .feature-grid-item {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 18px 16px;
        text-align: left;
        transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .feature-grid-item:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.07);
        border-color: #d1d5db;
    }
    .feature-grid-item .icon {
        font-size: 1.5rem;
        margin-bottom: 8px;
        display: block;
    }
    .feature-grid-item .label {
        font-size: 0.88rem;
        font-weight: 800;
        color: #111827;
        line-height: 1.3;
    }
    .feature-grid-item .desc {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 4px;
        line-height: 1.4;
    }

    /* =========================================================
       HEADINGS / TITLES
       ========================================================= */
    .section-title {
        font-size: clamp(1rem, 1.8vw, 1.15rem);
        font-weight: 900;
        color: #111827;
        margin-bottom: 0.9rem;
        margin-top: 0.25rem;
        word-wrap: break-word;
        letter-spacing: -0.01em;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    /* =========================================================
       CARDS
       ========================================================= */
    .top-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: clamp(18px, 3vw, 28px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.04);
        overflow: hidden;
        margin-bottom: 1.5rem;
    }

    .section-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: clamp(16px, 2.5vw, 24px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.03);
        overflow: hidden;
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 100%;
        margin-bottom: 1rem;
    }

    .section-card * {
        max-width: 100%;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    .summary-title {
        font-size: clamp(1.05rem, 2.4vw, 1.3rem);
        font-weight: 800;
        color: #111827;
        margin-bottom: 0.5rem;
        line-height: 1.3;
        word-wrap: break-word;
    }

    .summary-text {
        color: #6b7280;
        font-size: clamp(0.92rem, 1.8vw, 1rem);
        line-height: 1.7;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    /* =========================================================
       MATCH RING (RESPONSIVE)
       ========================================================= */
    .match-ring-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
    }

    .match-ring {
        width: clamp(140px, 25vw, 190px);
        height: clamp(140px, 25vw, 190px);
        border-radius: 50%;
        padding: 11px;
        margin: 0 auto;
        box-shadow: 0 8px 28px rgba(0,0,0,0.08);
        background: conic-gradient(#16a34a 0%, #16a34a 0%, #e5e7eb 0%, #e5e7eb 100%);
        display: flex;
        align-items: center;
        justify-content: center;
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
        font-size: clamp(2rem, 5vw, 3rem);
        font-weight: 900;
        line-height: 1;
        color: #16a34a;
        margin-bottom: 0.25rem;
    }

    .match-label {
        font-size: clamp(0.7rem, 1.4vw, 0.84rem);
        letter-spacing: 0.18em;
        color: #6b7280;
        font-weight: 800;
    }

    .match-badge {
        display: inline-block;
        margin-top: 12px;
        padding: 8px 14px;
        border-radius: 999px;
        color: white !important;
        font-weight: 700;
        font-size: 0.9rem;
        text-align: center;
    }

    /* =========================================================
       PROGRESS BARS
       ========================================================= */
    .bar-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 10px;
        overflow: hidden;
        max-width: 100%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }

    .bar-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
        font-size: clamp(0.85rem, 1.4vw, 0.92rem);
        font-weight: 800;
        color: #374151;
        margin-bottom: 10px;
        flex-wrap: wrap;
        word-wrap: break-word;
    }

    .bar-track {
        width: 100%;
        max-width: 100%;
        height: 10px;
        border-radius: 999px;
        background: #eef2f7;
        overflow: hidden;
    }

    .bar-fill {
        height: 100%;
        border-radius: 999px;
        transition: width 0.6s ease;
    }

    .bar-no-jd {
        color: #9ca3af;
        font-size: 0.88rem;
        font-style: italic;
        font-weight: 600;
    }

    /* =========================================================
       TABS  –  prevent hidden content, fix overflow
       ========================================================= */
    [data-testid="stTabsContent"] {
        overflow: visible !important;
    }
    [data-testid="stTabsContent"] > div {
        overflow: visible !important;
        max-width: 100% !important;
    }

    .section-card,
    .section-card *,
    [data-testid="stTabsContent"] > div,
    [data-testid="stTabsContent"] > div * {
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
    }

    /* Tab labels – keep readable */
    .stTabs [data-baseweb="tab-list"] button {
        color: #111827 !important;
        font-weight: 700;
        padding: 0.5rem 0.9rem;
    }
    .stTabs [aria-selected="true"] {
        color: #111827 !important;
    }

    /* =========================================================
       PILL TAGS
       ========================================================= */
    .pill {
        display: inline-block !important;
        visibility: visible !important;
        opacity: 1 !important;
        padding: 8px 14px;
        margin: 6px 8px 0 0;
        border-radius: 999px;
        font-size: clamp(0.82rem, 1.5vw, 0.92rem);
        font-weight: 800;
        color: white !important;
        box-shadow: 0 8px 18px rgba(0,0,0,0.08);
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 100%;
    }

    .tag-green  { background: linear-gradient(135deg, #16a34a, #22c55e); }
    .tag-red    { background: linear-gradient(135deg, #dc2626, #ef4444); }
    .tag-blue   { background: linear-gradient(135deg, #2563eb, #38bdf8); }
    .tag-gray   { background: linear-gradient(135deg, #475569, #64748b); }

    /* =========================================================
       FEATURE CARDS
       ========================================================= */
    .feature-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 18px;
        min-height: 135px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.03);
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    .feature-name {
        font-size: clamp(0.95rem, 1.8vw, 1.05rem);
        font-weight: 900;
        color: #111827;
        margin-bottom: 0.35rem;
    }

    .feature-desc {
        color: #6b7280;
        font-size: clamp(0.88rem, 1.6vw, 0.95rem);
        line-height: 1.6;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    /* =========================================================
       BUTTONS
       ========================================================= */
    .stButton > button {
        border: none;
        border-radius: 14px;
        padding: 0.85rem 1.5rem;
        font-size: 1.05rem;
        font-weight: 800;
        color: white !important;
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        box-shadow: 0 10px 24px rgba(17,24,39,0.15);
        width: 100%;
        max-width: 100%;
        transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
        position: relative;
        overflow: hidden;
        letter-spacing: 0.01em;
    }
    .stButton > button::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 32px rgba(17,24,39,0.2);
    }
    .stButton > button:hover::after {
        opacity: 1;
    }
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 6px 16px rgba(17,24,39,0.12);
    }
    .stButton > button * {
        position: relative;
        z-index: 1;
    }

    /* Landing page CTA container */
    .st-key-landing_card .stButton > button {
        max-width: 360px !important;
        margin: 0 auto !important;
    }

    /* =========================================================
       MARKDOWN / AI STREAMING REPORT
       ========================================================= */
    .stMarkdown, .stMarkdown > div, .stMarkdown p, .stMarkdown li,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    .stMarkdown code, .stMarkdown pre, .stMarkdown blockquote {
        color: #111827 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        max-width: 100% !important;
        white-space: normal !important;
    }

    .stMarkdown pre, .stMarkdown code {
        white-space: pre-wrap !important;
        word-break: break-word !important;
        overflow-x: auto !important;
        background: #f3f4f6;
        border-radius: 8px;
        padding: 8px 10px;
        font-size: 0.9rem;
    }

    /* Tables – align, wrap, prevent horizontal blowout */
    .stMarkdown table {
        width: 100% !important;
        max-width: 100% !important;
        table-layout: fixed !important;
        border-collapse: collapse !important;
        display: block;
        overflow-x: auto;
        word-wrap: break-word;
    }
    .stMarkdown table th,
    .stMarkdown table td {
        padding: 10px 12px !important;
        border: 1px solid #e5e7eb !important;
        text-align: left !important;
        vertical-align: top !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        color: #111827 !important;
        font-size: 0.95rem;
        line-height: 1.55;
    }
    .stMarkdown table th {
        background: #f9fafb !important;
        font-weight: 800 !important;
    }

    /* Lists – clean spacing */
    .stMarkdown ul, .stMarkdown ol {
        padding-left: 1.4rem !important;
        margin: 0.5rem 0 0.8rem 0 !important;
    }
    .stMarkdown li { margin-bottom: 0.25rem; }

    /* =========================================================
       CHAT / STREAMING MESSAGES
       ========================================================= */
    [data-testid="stChatMessage"],
    .stChatMessage {
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 14px !important;
        padding: 14px 16px !important;
        color: #111827 !important;
        max-width: 100% !important;
        overflow: hidden !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    [data-testid="stChatMessage"] * {
        color: #111827 !important;
        max-width: 100% !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }
    [data-testid="stChatMessage"] pre,
    [data-testid="stChatMessage"] code {
        white-space: pre-wrap !important;
        word-break: break-word !important;
        overflow-x: auto !important;
    }

    /* =========================================================
       COLUMNS  –  moderate gutter, no overlap / clipping
       ========================================================= */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 1.25rem;
        margin-bottom: 0.25rem;
    }
    [data-testid="stColumn"] {
        min-width: 0 !important;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    /* Landing page upload columns – equal width, tight alignment */
    .st-key-landing_card [data-testid="stHorizontalBlock"] {
        gap: 1.5rem !important;
        align-items: stretch !important;
    }
    .st-key-landing_card [data-testid="stColumn"] > div {
        height: 100% !important;
    }

    /* Vertical rhythm between Streamlit elements */
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.5rem;
    }

    /* =========================================================
       SMALLER ELEMENTS
       ========================================================= */
    .small-muted {
        color: #6b7280 !important;
        font-size: clamp(0.85rem, 1.5vw, 0.92rem);
        line-height: 1.5;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    /* =========================================================
       ERROR / SUCCESS / INFO  –  always visible text
       ========================================================= */
    .stAlert, .stAlert * {
        color: inherit !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    /* =========================================================
       SCROLLBAR / OVERFLOW SAFETY
       ========================================================= */
    .main, .stApp > div { overflow-x: hidden !important; }

    /* Streaming markdown container */
    .ai-stream-wrap {
        max-width: 100%;
        word-wrap: break-word;
        overflow-wrap: break-word;
        color: #111827;
        line-height: 1.65;
    }
    .ai-stream-wrap * {
        max-width: 100% !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }

    /* =========================================================
       RESPONSIVE BREAKPOINTS
       ========================================================= */
    @media (max-width: 992px) {
        .top-card { padding: 22px; }
        .section-card { padding: 20px; }
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: 1.25rem;
            padding-right: 1.25rem;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .top-card { padding: 18px; margin-bottom: 1.25rem; }
        .section-card { padding: 16px; margin-bottom: 0.9rem; }
        .bar-card { padding: 12px 16px; }
        [data-testid="stHorizontalBlock"] { gap: 0.9rem; }
        .stButton > button { width: 100%; }
        .feature-grid { grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.75rem; }
        .st-key-landing_card [data-testid="stHorizontalBlock"] { gap: 1rem !important; flex-direction: column !important; }
        .st-key-resume_upload_card, .st-key-job_upload_card { padding: 14px 16px 16px !important; }
    }

    @media (max-width: 480px) {
        .block-container {
            padding-left: 0.9rem;
            padding-right: 0.9rem;
        }
        .top-card { padding: 16px; border-radius: 16px; }
        .section-card { padding: 14px; border-radius: 14px; }
        .main-title { font-size: 1.5rem; }
        .sub-title { margin-bottom: 1.25rem; }
        .pill { font-size: 0.8rem; padding: 5px 10px; margin: 4px 5px 0 0; }
        [data-testid="stHorizontalBlock"] { gap: 0.6rem; }
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
# TITLE / HERO
# -----------------------------------
st.markdown('<div class="ai-badge">AI-Powered Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="main-title">Job <span class="gradient">Match</span> Analyzer</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-title">Upload your resume and job description and get an instant ATS compatibility score with AI-driven insights.</div>',
    unsafe_allow_html=True
)


# -----------------------------------
# BEFORE ANALYSIS
# -----------------------------------
if not st.session_state.analyzed:

    with st.container(key="landing_card"):
        st.markdown(
            '<div class="upload-section-title">📎 Upload Documents</div>',
            unsafe_allow_html=True
        )

        col_a, col_b = st.columns([1, 1])

        with col_a:
            with st.container(key="resume_upload_card"):
                resume_file = st.file_uploader("📄 Upload Resume", type=["txt"])
                st.markdown('<span class="upload-note">⏺ Supports .txt files</span>', unsafe_allow_html=True)

        with col_b:
            with st.container(key="job_upload_card"):
                job_file = st.file_uploader("📋 Upload Job Description", type=["txt"])
                st.markdown('<span class="upload-note">⏺ Supports .txt files</span>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top: 1.75rem;"></div>', unsafe_allow_html=True)

        analyze_clicked = st.button("🔍 Analyze Match")

    # --------------------------------------------------
    # FEATURE GRID
    # --------------------------------------------------
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

    st.markdown(
        '<div class="section-title">AI Resume Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="small-muted">
        Generate professional AI-powered resume feedback using OpenRouter.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Generate AI Suggestions"):

        with st.spinner("AI is analyzing the resume..."):

            try:

                # Reduce token usage
                short_resume = resume_text[:5000]
                short_job = job_text[:5000]

                prompt = f"""
                You are an elite ATS optimization expert and senior technical recruiter with 15+ years of experience at top tech companies like Google, Microsoft, and Amazon.

                A candidate has submitted their resume for a specific job role. Your task is to provide a deeply analytical, actionable, and honest evaluation.

                ---
                RESUME:
                {short_resume}

                ---
                JOB DESCRIPTION:
                {short_job}

                ---

                Carefully analyze the resume against the job description and return a structured report with the following 7 sections. Be specific, honest, and use examples directly from the resume where possible.

                ---

                ### 1. 🎯 ATS Improvement Suggestions
                - List specific formatting, keyword, and structural changes needed to pass ATS filters.
                - Mention exact section headers, date formats, and layout improvements.

                ### 2. 🔑 Missing Important Keywords
                - List keywords, tools, technologies, and phrases from the job description that are absent in the resume.
                - Group them as: **Technical Skills | Soft Skills | Domain Terms**

                ### 3. ✅ Resume Strengths
                - Highlight what the candidate has done well.
                - Be specific — mention actual skills, experiences, or formatting choices that stand out.

                ### 4. ⚠️ Resume Weaknesses
                - Be direct and honest about gaps, vague statements, or missing quantifications.
                - Suggest how each weakness can be fixed with a concrete example.

                ### 5. 🎤 Interview Preparation Tips
                - Based on the job description, list the top 5 questions the candidate is likely to face.
                - For each question, give a 1-line tip on how to answer it using their resume experience.

                ### 6. 🚀 Recommended Projects
                - Suggest 3–5 specific projects the candidate should build or showcase to strengthen their profile for this role.
                - Include the tech stack for each project.

                ### 7. 📈 Career Improvement Suggestions
                - Give a honest, motivating roadmap: certifications, skills to learn, communities to join, and timeline estimates.

                ---

                Format your response using clear markdown with bold headings, bullet points, and emojis as shown above.
                Be direct, specific, and encouraging. Avoid generic advice — everything must be tailored to THIS resume and THIS job.
                """

                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    streamed_text = ""

                    for chunk in ask_ai_stream(prompt):
                        streamed_text += chunk
                        message_placeholder.markdown(
                            f'<div class="ai-stream-wrap">{streamed_text}</div>',
                            unsafe_allow_html=True
                        )

                st.success("AI Analysis Complete")

            except Exception as e:
                st.error(f"AI Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------
# AI SUGGESTIONS
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
# RESET
# -----------------------------------
st.markdown("<br>", unsafe_allow_html=True)
if st.button("Analyze Another Resume"):
    reset_app()
    st.rerun()
