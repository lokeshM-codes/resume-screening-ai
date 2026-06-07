# AI Resume Analyzer

An elegant, modular, startup-level ATS Resume Analyzer built with **Streamlit** and **OpenRouter AI** (GPT-OSS). It calculates keyword match ratios (technical skills, soft skills, experience, education), computes text similarity using TF-IDF cosine similarity, and streams detailed optimization recommendations.

---

## 📂 Project Architecture

```
project/
│
├── app.py                         # Main entry point (Streamlit UI layout)
│
├── components/
│   ├── upload_section.py          # Hero, File Uploaders, and file validation
│   ├── match_dashboard.py         # Top match ring, status card, and breakdown bars
│   ├── skill_analysis.py          # Skills tab (Matched & Missing skills)
│   ├── experience_analysis.py     # Experience tab (Matched & Missing experience terms)
│   ├── education_analysis.py      # Education tab (Matched & Missing education terms)
│   ├── ai_assistant.py            # AI Features tab (AI suggestions from OpenRouter)
│   ├── chatbot.py                 # Chatbot tab (Interactive QA about the resume)
│   └── reusable_ui.py             # Reusable UI widgets, rendering helpers, and CSS loader
│
├── services/
│   ├── resume_analyzer.py         # Main analyzer service logic
│   ├── ai_service.py              # Interface to OpenRouter client
│   ├── text_processing.py         # Text cleaning and keyword extraction
│   └── scoring.py                 # Scoring calculations & weights
│
├── config/
│   ├── settings.py                # Upload limits, model configurations, URLs
│   ├── prompts.py                 # Detailed AI system/user prompts
│   └── constants.py               # Page configuration, colors, session state constants
│
├── styles/
│   └── main.css                   # Consolidated external CSS stylesheet
│
├── utils/
│   ├── helpers.py                 # Formatting, score label helpers
│   ├── validators.py              # File size and type validators
│   └── file_handler.py            # Text decoding and file reader
│
├── data/
│   ├── technical_skills.py        # Technical skills vocabulary
│   ├── soft_skills.py             # Soft skills vocabulary
│   └── education_keywords.py      # Experience and education terms
│
├── requirements.txt               # pip requirements file
└── README.md                      # Documentation
```

---

## 🛠 Features & Modular Separation

1. **Modular UI Components (`components/`)**:
   - Every view state (upload page vs dashboard page) and tab item (Skills, Experience, Education, AI, Chatbot) is separated into its own module file.
2. **Centralized CSS (`styles/main.css`)**:
   - No styling mixed with Python logic. The style block has been migrated into `styles/main.css` and loaded automatically via a helper function inside `components/reusable_ui.py`.
3. **Editable Configurations (`config/settings.py`)**:
   - Change upload limits (`MAX_UPLOAD_MB = 20`) or OpenRouter completion properties (default models, endpoints, temperatures) in one single place.
4. **Keyword Datasets (`data/`)**:
   - Easily modify the core vocabulary lists used by the analyzer to filter technical/soft skills or experience/education keywords.
5. **Interactive Chatbot (`components/chatbot.py`)**:
   - Let candidates converse directly with the AI assistant about how their resume aligns with the job description.

---

## 🚀 Setup & Execution

### 1. Install Dependencies
Ensure you have Python 3.8+ installed. Install the required libraries:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory and add your OpenRouter API key:
```env
OPENROUTER_API_KEY="your-openrouter-api-key-here"
```

### 3. Run the Application
Start the Streamlit development server:
```bash
streamlit run app.py
```
This will start the application locally and open a window in your default web browser (usually at `http://localhost:8501`).
