# =============================================================================
# app.py — ResumeAI | Complete End-to-End ATS Resume Matcher
# =============================================================================

import streamlit as st
from config import APP_VERSION

st.set_page_config(
    page_title="ResumeAI — ATS Resume Matcher",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session State ─────────────────────────────────────────────────────────────
for key, val in {"page": "home", "results": None, "parsed": None}.items():
    if key not in st.session_state:
        st.session_state[key] = val 

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, .stApp, [data-theme="dark"], [data-theme="light"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #FFFFFF !important;
    color: #111827 !important;
}
section[data-testid="stSidebar"] { display: none !important; }
footer { visibility: hidden !important; }
.main .block-container {
    padding: 0 2.5rem 4rem 2.5rem !important;
    max-width: 1200px !important;
}

/* All text dark */
h1,h2,h3,h4,h5,p,span,label,div { color: inherit; }

/* Nav buttons */
.nav-btn button {
    background: transparent !important;
    border: none !important;
    color: #6B7280 !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    padding: 0.4rem 0.9rem !important;
    border-radius: 6px !important;
    width: 100% !important;
    font-family: 'Inter', sans-serif !important;
}
.nav-btn button:hover {
    background: #F3F4F6 !important;
    color: #111827 !important;
}
.nav-btn-active button {
    background: #EEF2FF !important;
    color: #4F46E5 !important;
    font-weight: 600 !important;
    border: none !important;
    font-size: 0.875rem !important;
    padding: 0.4rem 0.9rem !important;
    border-radius: 6px !important;
    width: 100% !important;
    font-family: 'Inter', sans-serif !important;
}

/* Primary button */
.stButton > button[kind="primary"] {
    background: #6366F1 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 2rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"]:hover {
    background: #4F46E5 !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.4) !important;
    transform: translateY(-1px) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #F9FAFB !important;
    border: 2px dashed #C7D2FE !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #6366F1 !important;
    background: #F5F3FF !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] p,
[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: #6B7280 !important;
}

/* Textarea */
.stTextArea textarea {
    background: #F9FAFB !important;
    border: 1.5px solid #E5E7EB !important;
    border-radius: 10px !important;
    color: #111827 !important;
    font-size: 0.875rem !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextArea textarea:focus {
    border-color: #6366F1 !important;
    background: #FFFFFF !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}
.stTextArea textarea::placeholder { color: #9CA3AF !important; }

/* Metrics */
[data-testid="stMetric"] {
    background: #F9FAFB !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    padding: 1.25rem 1rem !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    color: #111827 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.7px !important;
    color: #6B7280 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #F3F4F6 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 0 !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 7px !important;
    color: #6B7280 !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    border: none !important;
    font-family: 'Inter', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #111827 !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.09) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #F9FAFB !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    color: #111827 !important;
    border: 1px solid #E5E7EB !important;
    font-family: 'Inter', sans-serif !important;
}

/* Spinner */
.stSpinner { color: #6366F1 !important; }

/* Success / Error */
.stSuccess > div { background: #F0FDF4 !important; color: #166534 !important; border-radius: 8px !important; }
.stError   > div { background: #FFF1F2 !important; color: #9F1239 !important; border-radius: 8px !important; }
.stInfo    > div { background: #EFF6FF !important; color: #1E40AF !important; border-radius: 8px !important; }
.stWarning > div { background: #FFFBEB !important; color: #92400E !important; border-radius: 8px !important; }

/* Download button */
.stDownloadButton > button {
    background: #111827 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.55rem 1.5rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: #374151 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def chips(items, bg, fg, border):
    if not items:
        st.markdown("<p style='color:#9CA3AF;font-size:0.85rem;'>None found.</p>", unsafe_allow_html=True)
        return
    html = " ".join([
        f'<span style="display:inline-block;background:{bg};color:{fg};'
        f'border:1px solid {border};border-radius:6px;padding:0.25rem 0.65rem;'
        f'font-size:0.78rem;font-weight:500;margin:0.2rem 0.1rem;">{s}</span>'
        for s in items
    ])
    st.markdown(html, unsafe_allow_html=True)


def section_title(text):
    st.markdown(
        f"<p style='font-size:0.72rem;font-weight:700;color:#6366F1;"
        f"letter-spacing:1.4px;text-transform:uppercase;margin:0 0 4px;'>{text}</p>",
        unsafe_allow_html=True
    )


def card_start(padding="1.5rem"):
    st.markdown(
        f"<div style='background:white;border-radius:14px;"
        f"border:1px solid #E5E7EB;padding:{padding};margin-bottom:1.25rem;'>",
        unsafe_allow_html=True
    )


def card_end():
    st.markdown("</div>", unsafe_allow_html=True)


def divider():
    st.markdown(
        "<hr style='border:none;border-top:1px solid #F3F4F6;margin:1.25rem 0;'>",
        unsafe_allow_html=True
    )


# ── Top Navigation ────────────────────────────────────────────────────────────
def topnav():
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    c_logo, c_nav, c_right = st.columns([2, 5, 2])

    with c_logo:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:9px;padding-top:4px;">
            <div style="width:34px;height:34px;background:#6366F1;border-radius:9px;
                 display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <span style="color:white;font-weight:800;font-size:1rem;line-height:1;">R</span>
            </div>
            <span style="font-size:1.05rem;font-weight:700;color:#111827;">ResumeAI</span>
        </div>
        """, unsafe_allow_html=True)

    with c_nav:
        pages = [
            ("🏠 Home",        "home"),
            ("⚡ ATS Matcher", "matcher"),
            ("📊 History",     "history"),
            ("ℹ️ About",       "about"),
        ]
        cols = st.columns(len(pages))
        for col, (label, key) in zip(cols, pages):
            with col:
                is_active = st.session_state.page == key
                css_class = "nav-btn-active" if is_active else "nav-btn"
                st.markdown(f"<div class='{css_class}'>", unsafe_allow_html=True)
                if st.button(label, key=f"nav_{key}"):
                    st.session_state.page = key
                    if key != "matcher":
                        st.session_state.results = None
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    with c_right:
        st.markdown(f"""
        <div style="text-align:right;padding-top:7px;">
            <span style="background:#EEF2FF;color:#4F46E5;font-size:0.72rem;
                 font-weight:600;padding:4px 12px;border-radius:999px;
                 letter-spacing:0.3px;">v{APP_VERSION}</span>
        </div>
        """, unsafe_allow_html=True)

    divider()


# ── HOME PAGE ─────────────────────────────────────────────────────────────────
def page_home():
    # Hero
    st.markdown("""
    <div style="background:linear-gradient(135deg,#6366F1 0%,#8B5CF6 100%);
         border-radius:16px;padding:3rem 3rem;color:white;margin-bottom:1.75rem;">
        <p style="font-size:0.72rem;font-weight:600;letter-spacing:2px;
             opacity:0.65;margin:0 0 0.6rem;text-transform:uppercase;color:white;">
            Resume Intelligence Platform
        </p>
        <h1 style="font-size:2.1rem;font-weight:800;letter-spacing:-1px;
             line-height:1.25;margin:0 0 0.9rem;color:white;">
            Land more interviews<br/>with a better resume.
        </h1>
        <p style="font-size:0.92rem;opacity:0.85;line-height:1.75;
             max-width:500px;margin:0 0 1.75rem;color:white;">
            AI-powered ATS scanner — upload your resume, paste any job description,
            and get your match score, skill gaps, and actionable fixes instantly.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Stat cards
    cards = [
        ("📄","#EEF2FF","Formats Supported","PDF & DOCX"),
        ("🧠","#F0FDF4","ML Engine","TF-IDF + NLP"),
        ("⚡","#FFFBEB","Skills Database","200+ Skills"),
        ("📊","#FFF1F2","Report Export","PDF Download"),
    ]
    cols = st.columns(4)
    for col, (icon, bg, label, val) in zip(cols, cards):
        with col:
            st.markdown(f"""
            <div style="background:white;border-radius:13px;padding:1.2rem;
                 border:1px solid #E5E7EB;display:flex;align-items:center;gap:0.9rem;">
                <div style="width:44px;height:44px;border-radius:11px;background:{bg};
                     display:flex;align-items:center;justify-content:center;
                     font-size:1.25rem;flex-shrink:0;">{icon}</div>
                <div>
                    <div style="font-size:0.67rem;font-weight:600;color:#9CA3AF;
                         letter-spacing:0.8px;text-transform:uppercase;margin-bottom:3px;">
                         {label}</div>
                    <div style="font-size:1rem;font-weight:700;color:#111827;">{val}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # How it works
    card_start()
    st.markdown("<p style='font-size:1rem;font-weight:700;color:#111827;margin:0 0 1.25rem;'>🔄 How it works</p>", unsafe_allow_html=True)
    steps = [
        ("01","Upload Resume","PDF or DOCX, any format"),
        ("02","Paste Job Description","From LinkedIn, Naukri, etc."),
        ("03","AI Analysis Runs","NLP + ML engine processes"),
        ("04","Get Full Report","Score, gaps, tips, PDF"),
    ]
    s_cols = st.columns(4)
    for col, (num, title, desc) in zip(s_cols, steps):
        with col:
            st.markdown(f"""
            <div style="text-align:center;padding:0.5rem 0.25rem 1rem;">
                <div style="width:38px;height:38px;border-radius:50%;background:#6366F1;
                     color:white;font-weight:700;font-size:0.78rem;display:flex;
                     align-items:center;justify-content:center;margin:0 auto 0.7rem;">{num}</div>
                <div style="font-weight:600;color:#111827;font-size:0.875rem;
                     margin-bottom:0.3rem;">{title}</div>
                <div style="font-size:0.78rem;color:#9CA3AF;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    card_end()

    # CTA button
    _, mid, _ = st.columns([1.5, 1, 1.5])
    with mid:
        if st.button("⚡  Start Analyzing →", type="primary", use_container_width=True):
            st.session_state.page = "matcher"
            st.rerun()


# ── MATCHER PAGE ──────────────────────────────────────────────────────────────
def page_matcher():
    section_title("Free Tool")
    st.markdown("""
    <h1 style="font-size:1.8rem;font-weight:800;color:#111827;
         letter-spacing:-0.8px;margin:0 0 8px;">
        Resume & Job Description Matcher
    </h1>
    <p style="font-size:0.92rem;color:#6B7280;margin:0 0 1.75rem;
         line-height:1.7;max-width:560px;">
        Upload your resume and paste a job description to get your ATS score,
        missing keywords, skill gaps, and improvement tips.
    </p>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        card_start()
        st.markdown("""
        <p style="font-size:0.7rem;font-weight:700;color:#374151;
             letter-spacing:1px;text-transform:uppercase;margin-bottom:3px;">Your Resume</p>
        <p style="font-size:1rem;font-weight:600;color:#111827;margin-bottom:10px;">
            Upload your resume</p>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "resume_upload", type=["pdf","docx"],
            label_visibility="collapsed"
        )
        if uploaded_file:
            st.success(f"✓ **{uploaded_file.name}** ready for analysis")
        else:
            st.caption("📎 Supports PDF and DOCX · Max 5MB · Text-based only")
        card_end()

    with col_r:
        card_start()
        st.markdown("""
        <p style="font-size:0.7rem;font-weight:700;color:#374151;
             letter-spacing:1px;text-transform:uppercase;margin-bottom:3px;">Job Description</p>
        <p style="font-size:1rem;font-weight:600;color:#111827;margin-bottom:10px;">
            Paste the job description</p>
        """, unsafe_allow_html=True)
        job_desc = st.text_area(
            "jd_input", height=185,
            placeholder="Paste the full job description here...\n\nExample:\nWe are looking for a Python Developer with 2+ years experience in Django, REST APIs, PostgreSQL, Docker...",
            label_visibility="collapsed",
        )
        if job_desc.strip():
            wc = len(job_desc.split())
            st.caption(f"📝 {wc} words entered")
        card_end()

    divider()

    _, mid, _ = st.columns([1.5, 1, 1.5])
    with mid:
        run = st.button("⚡  Analyze & Compare", type="primary", use_container_width=True)

    if run:
        if not uploaded_file:
            st.error("⚠️ Please upload your resume (PDF or DOCX) to continue.")
            return
        if not job_desc.strip():
            st.error("⚠️ Please paste a job description to continue.")
            return

        with st.spinner("🔍 Analyzing your resume against the job description..."):
            from utils.resume_parser import parse_resume
            from utils.matcher import match as run_match
            from database.database import save_analysis

            parsed  = parse_resume(uploaded_file)
            results = run_match(parsed["raw_text"], job_desc)
            st.session_state.parsed  = parsed
            st.session_state.results = results
            save_analysis(parsed, results)

        st.rerun()

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.results and st.session_state.parsed:
        show_results(st.session_state.results, st.session_state.parsed)


# ── RESULTS SECTION ───────────────────────────────────────────────────────────
def show_results(r, parsed):
    divider()

    # Header
    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;
         margin-bottom:1.4rem;flex-wrap:wrap;gap:0.5rem;">
        <div>
            <h2 style="font-size:1.3rem;font-weight:700;color:#111827;margin:0 0 3px;">
                Analysis Results</h2>
            <p style="font-size:0.82rem;color:#9CA3AF;margin:0;">
                {parsed.get('name','—')} &nbsp;·&nbsp;
                {parsed.get('email','—')} &nbsp;·&nbsp;
                {parsed.get('word_count',0):,} words in resume
            </p>
        </div>
        <div style="background:{r['color']}18;border:1.5px solid {r['color']}55;
             border-radius:999px;padding:0.4rem 1.2rem;">
            <span style="color:{r['color']};font-weight:700;font-size:0.875rem;">
                {r['label']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("ATS Match Score",   f"{r['ats_score']}%")
    with m2: st.metric("Skills Matched",    len(r['matched_skills']))
    with m3: st.metric("Keywords Matched",  f"{r['keyword_match_pct']}%")
    with m4: st.metric("Resume Quality",    f"{r['quality_score']}%")

    st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

    # Score bars
    card_start()
    for label, score, color in [
        ("ATS Match Score",  r['ats_score'],    r['color']),
        ("Resume Quality",   r['quality_score'], "#6366F1"),
        ("Keyword Coverage", r['keyword_match_pct'], "#F59E0B"),
    ]:
        pct = min(score, 100)
        st.markdown(f"""
        <div style="margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;
                 margin-bottom:5px;">
                <span style="font-size:0.85rem;font-weight:500;color:#374151;">
                    {label}</span>
                <span style="font-size:0.85rem;font-weight:700;color:{color};">
                    {score}%</span>
            </div>
            <div style="background:#F3F4F6;border-radius:999px;height:8px;">
                <div style="width:{pct}%;background:{color};
                     border-radius:999px;height:8px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    card_end()

    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "✅ Matched Skills",
        "❌ Missing Skills",
        "🔑 Keywords",
        "💡 Suggestions",
        "🎯 Job Roles",
        "👤 Resume Info",
    ])

    with tab1:
        st.markdown(f"<p style='font-size:0.85rem;color:#6B7280;margin-bottom:0.75rem;'>"
                    f"{len(r['matched_skills'])} skills found in both your resume and the job description</p>",
                    unsafe_allow_html=True)
        if r["matched_skills"]:
            chips(r["matched_skills"], "#F0FDF4", "#166534", "#BBF7D0")
        else:
            st.warning("No overlapping skills found. Add more relevant skills to your resume.")

    with tab2:
        st.markdown(f"<p style='font-size:0.85rem;color:#6B7280;margin-bottom:0.75rem;'>"
                    f"{len(r['missing_skills'])} skills from the JD are missing in your resume</p>",
                    unsafe_allow_html=True)
        if r["missing_skills"]:
            chips(r["missing_skills"], "#FFF1F2", "#9F1239", "#FECDD3")
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            st.info("💡 Add these skills to your resume if you have experience with them.")
        else:
            st.success("🎉 Your resume covers all skills mentioned in the job description!")

    with tab3:
        kc1, kc2 = st.columns(2, gap="large")
        with kc1:
            st.markdown("<p style='font-weight:600;color:#111827;font-size:0.875rem;"
                        "margin-bottom:0.6rem;'>✅ Matched Keywords</p>", unsafe_allow_html=True)
            chips(r["matched_keywords"], "#EEF2FF", "#3730A3", "#C7D2FE")
        with kc2:
            st.markdown("<p style='font-weight:600;color:#111827;font-size:0.875rem;"
                        "margin-bottom:0.6rem;'>❌ Missing Keywords</p>", unsafe_allow_html=True)
            chips(r["missing_keywords"], "#FFF1F2", "#9F1239", "#FECDD3")

    with tab4:
        for i, tip in enumerate(r.get("suggestions", []), 1):
            st.markdown(f"""
            <div style="background:#F9FAFB;border-radius:10px;border:1px solid #E5E7EB;
                 padding:1rem 1.25rem;margin-bottom:0.75rem;display:flex;gap:1rem;
                 align-items:flex-start;">
                <div style="width:26px;height:26px;border-radius:50%;background:#6366F1;
                     color:white;font-size:0.75rem;font-weight:700;display:flex;
                     align-items:center;justify-content:center;flex-shrink:0;">{i}</div>
                <p style="font-size:0.875rem;color:#374151;margin:0;line-height:1.6;">{tip}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab5:
        roles = r.get("suggested_roles", [])
        if roles:
            st.markdown("<p style='font-size:0.85rem;color:#6B7280;margin-bottom:0.75rem;'>"
                        "Based on your skills, you best match these roles:</p>",
                        unsafe_allow_html=True)
            for role, pct in roles:
                color = "#16A34A" if pct >= 70 else "#D97706" if pct >= 40 else "#9CA3AF"
                st.markdown(f"""
                <div style="margin-bottom:0.75rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                        <span style="font-size:0.875rem;font-weight:500;color:#111827;">{role}</span>
                        <span style="font-size:0.875rem;font-weight:700;color:{color};">{pct}%</span>
                    </div>
                    <div style="background:#F3F4F6;border-radius:999px;height:7px;">
                        <div style="width:{pct}%;background:{color};border-radius:999px;height:7px;">
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No role predictions available. Add more technical skills to your resume.")

    with tab6:
        ti1, ti2 = st.columns(2, gap="large")
        with ti1:
            st.markdown("""
            <p style="font-size:0.7rem;font-weight:700;color:#9CA3AF;
                 text-transform:uppercase;letter-spacing:0.8px;margin-bottom:0.75rem;">
                Contact Information</p>
            """, unsafe_allow_html=True)
            for label, val in [
                ("Name",     parsed.get("name","—")),
                ("Email",    parsed.get("email","—")),
                ("Phone",    parsed.get("phone","—")),
                ("LinkedIn", parsed.get("linkedin","—")),
                ("GitHub",   parsed.get("github","—")),
            ]:
                st.markdown(f"""
                <div style="display:flex;gap:0.75rem;padding:0.5rem 0;
                     border-bottom:1px solid #F3F4F6;">
                    <span style="font-size:0.82rem;font-weight:600;color:#6B7280;
                         min-width:70px;">{label}</span>
                    <span style="font-size:0.82rem;color:#111827;">{val}</span>
                </div>
                """, unsafe_allow_html=True)

        with ti2:
            sk = r["resume_skills"]
            st.markdown("""
            <p style="font-size:0.7rem;font-weight:700;color:#9CA3AF;
                 text-transform:uppercase;letter-spacing:0.8px;margin-bottom:0.75rem;">
                Skills Detected in Resume</p>
            """, unsafe_allow_html=True)
            for label, items in [
                ("Languages",   sk["programming_languages"]),
                ("Frameworks",  sk["frameworks"]),
                ("Databases",   sk["databases"]),
                ("Cloud/DevOps",sk["cloud_devops"]),
                ("Tools",       sk["tools"]),
            ]:
                val = ", ".join(items) if items else "—"
                st.markdown(f"""
                <div style="display:flex;gap:0.75rem;padding:0.5rem 0;
                     border-bottom:1px solid #F3F4F6;flex-wrap:wrap;">
                    <span style="font-size:0.82rem;font-weight:600;color:#6B7280;
                         min-width:90px;">{label}</span>
                    <span style="font-size:0.82rem;color:#111827;flex:1;">{val}</span>
                </div>
                """, unsafe_allow_html=True)

    # PDF Download
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    divider()
    st.markdown("<p style='font-size:0.875rem;font-weight:600;color:#111827;margin-bottom:0.75rem;'>📥 Download Report</p>", unsafe_allow_html=True)

    try:
        from utils.report_generator import generate_pdf_report
        pdf_bytes = generate_pdf_report(parsed, r)
        dl1, dl2, _ = st.columns([1, 1, 2])
        with dl1:
            st.download_button(
                label="⬇️  Download PDF Report",
                data=pdf_bytes,
                file_name=f"ResumeAI_Report_{parsed.get('name','Candidate').replace(' ','_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        with dl2:
            if st.button("🔄  Analyze Another Resume", use_container_width=True):
                st.session_state.results = None
                st.session_state.parsed  = None
                st.rerun()
    except Exception as e:
        st.error(f"PDF generation error: {e}")


# ── HISTORY PAGE ──────────────────────────────────────────────────────────────
def page_history():
    from database.database import get_all_analyses, delete_analysis, clear_all
    import json

    st.markdown("""
    <h1 style="font-size:1.6rem;font-weight:800;color:#111827;margin:0 0 4px;">
        Analysis History</h1>
    <p style="font-size:0.875rem;color:#6B7280;margin:0 0 1.5rem;">
        All your past resume analyses stored locally.</p>
    """, unsafe_allow_html=True)

    rows = get_all_analyses()

    if not rows:
        st.markdown("""
        <div style="background:white;border-radius:14px;border:1px solid #E5E7EB;
             padding:4rem 2rem;text-align:center;">
            <div style="font-size:2.5rem;margin-bottom:1rem;">🗂️</div>
            <p style="font-size:1rem;font-weight:600;color:#374151;margin-bottom:0.5rem;">
                No analyses yet</p>
            <p style="font-size:0.85rem;color:#9CA3AF;">
                Run your first analysis on the ATS Matcher page.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Summary stats
    avg_ats = round(sum(r[3] for r in rows) / len(rows), 1)
    best    = max(rows, key=lambda x: x[3])
    s1, s2, s3 = st.columns(3)
    with s1: st.metric("Total Analyses", len(rows))
    with s2: st.metric("Average ATS Score", f"{avg_ats}%")
    with s3: st.metric("Best Score", f"{best[3]}% ({best[1]})")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    for row in rows:
        rid, name, fname, ats, quality, label, matched_s, missing_s, roles, date = row
        color = "#16A34A" if ats >= 80 else "#D97706" if ats >= 60 else "#EA580C" if ats >= 40 else "#DC2626"
        matched = json.loads(matched_s) if matched_s else []
        missing = json.loads(missing_s) if missing_s else []

        with st.expander(f"📄 {name} — {fname}  |  ATS: {ats}%  |  {date}"):
            hc1, hc2, hc3 = st.columns(3)
            with hc1: st.metric("ATS Score",  f"{ats}%")
            with hc2: st.metric("Quality",    f"{quality}%")
            with hc3:
                st.markdown(f"""
                <div style="background:{color}18;border:1px solid {color}55;
                     border-radius:8px;padding:0.75rem;text-align:center;margin-top:0.25rem;">
                    <span style="color:{color};font-weight:700;font-size:0.875rem;">{label}</span>
                </div>
                """, unsafe_allow_html=True)

            if matched:
                st.markdown("<p style='font-size:0.82rem;font-weight:600;color:#374151;"
                            "margin:0.75rem 0 0.4rem;'>Matched Skills</p>", unsafe_allow_html=True)
                chips(matched[:10], "#F0FDF4", "#166534", "#BBF7D0")
            if missing:
                st.markdown("<p style='font-size:0.82rem;font-weight:600;color:#374151;"
                            "margin:0.75rem 0 0.4rem;'>Missing Skills</p>", unsafe_allow_html=True)
                chips(missing[:10], "#FFF1F2", "#9F1239", "#FECDD3")

            if st.button(f"🗑️ Delete", key=f"del_{rid}"):
                delete_analysis(rid)
                st.rerun()

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    if st.button("🗑️  Clear All History"):
        clear_all()
        st.rerun()


# ── ABOUT PAGE ────────────────────────────────────────────────────────────────
def page_about():
    st.markdown("""
    <h1 style="font-size:1.6rem;font-weight:800;color:#111827;margin:0 0 1.5rem;">
        About ResumeAI</h1>
    """, unsafe_allow_html=True)

    card_start("2rem")
    st.markdown("""
    <p style="font-size:1rem;font-weight:700;color:#111827;margin-bottom:0.75rem;">
        ⚡ ResumeAI — AI Resume Screening & Job Match System</p>
    <p style="font-size:0.9rem;color:#6B7280;line-height:1.85;margin-bottom:1.25rem;">
        A production-quality AI-powered Applicant Tracking System (ATS) built as a
        Final Year B.Tech CSE (AI & ML) project. Demonstrates real-world skills in
        NLP, Machine Learning, full-stack Python development, and database management.
    </p>
    """, unsafe_allow_html=True)

    for title, items in [
        ("🛠 Tech Stack", [
            ("Language",        "Python 3.11"),
            ("UI Framework",    "Streamlit 1.32"),
            ("NLP",             "spaCy, NLTK"),
            ("ML",              "scikit-learn (TF-IDF + Cosine Similarity)"),
            ("PDF Parsing",     "pdfplumber"),
            ("DOCX Parsing",    "python-docx"),
            ("Visualization",   "Plotly, Matplotlib"),
            ("Database",        "SQLite"),
            ("PDF Reports",     "ReportLab"),
        ]),
        ("📦 Modules", [
            ("resume_parser.py",    "PDF & DOCX text extraction + contact info"),
            ("skill_extractor.py",  "200+ skills detection (languages, frameworks, tools)"),
            ("matcher.py",          "TF-IDF + Cosine Similarity ATS engine"),
            ("database.py",         "SQLite history store"),
            ("report_generator.py", "Professional PDF report generation"),
        ]),
    ]:
        st.markdown(f"<p style='font-size:0.82rem;font-weight:700;color:#6366F1;"
                    f"text-transform:uppercase;letter-spacing:1px;margin:1rem 0 0.6rem;'>{title}</p>",
                    unsafe_allow_html=True)
        for k, v in items:
            st.markdown(f"""
            <div style="display:flex;gap:1rem;padding:0.45rem 0;
                 border-bottom:1px solid #F3F4F6;">
                <span style="font-size:0.82rem;font-weight:600;color:#374151;
                     min-width:180px;">{k}</span>
                <span style="font-size:0.82rem;color:#6B7280;">{v}</span>
            </div>
            """, unsafe_allow_html=True)
    card_end()


# ── ROUTER ────────────────────────────────────────────────────────────────────
def main():
    topnav()
    page = st.session_state.page
    if   page == "home":    page_home()
    elif page == "matcher": page_matcher()
    elif page == "history": page_history()
    elif page == "about":   page_about()
    else:                   page_home()


if __name__ == "__main__":
    main()
