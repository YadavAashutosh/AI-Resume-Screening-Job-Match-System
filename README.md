# ⚡ ResumeAI — AI Resume Screening & Job Match System

A production-quality AI-powered ATS (Applicant Tracking System) built as a Final Year B.Tech CSE (AI & ML) project.

---

## 🚀 Features

- 📄 Resume parsing — PDF & DOCX
- 🧠 TF-IDF + Cosine Similarity ML engine
- 📊 Real ATS score calculation
- 🔍 200+ skills detection
- 🎯 Job role prediction
- 💡 Personalized improvement suggestions
- 🗂️ SQLite analysis history
- 📥 PDF report download
- 🧭 Multi-page navigation

---

## ⚙️ Setup

```bash
# 1. Clone / extract project
cd AI-Resume-Screening-System

# 2. Create virtual environment with Python 3.11
py -3.11 -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install spaCy model
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

# 5. Download NLTK data
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt')"

# 6. Run
streamlit run app.py
```

---

## 📁 Structure

```
resumeai/
├── app.py                      # Main Streamlit app
├── config.py                   # Central config + skills DB
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml             # Light theme force
├── utils/
│   ├── resume_parser.py        # PDF + DOCX extraction
│   ├── skill_extractor.py      # 200+ skill detection
│   ├── matcher.py              # TF-IDF ATS engine
│   └── report_generator.py     # PDF report
├── database/
│   └── database.py             # SQLite history
├── uploads/
└── reports/
```

---

## 🛠 Tech Stack

Python · Streamlit · spaCy · scikit-learn · NLTK · pdfplumber · python-docx · SQLite · ReportLab · Plotly

---


