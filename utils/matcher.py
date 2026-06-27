# =============================================================================
# utils/matcher.py — TF-IDF + Cosine Similarity ATS Engine
# =============================================================================
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.skill_extractor import extract_skills
from config import JOB_ROLES


def _clean(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def _quality_score(text: str, skills: dict) -> int:
    score = 0
    t = text.lower()
    if len(text) > 300:  score += 15
    if len(text) > 800:  score += 10
    if skills["total_count"] >= 5:  score += 15
    if skills["total_count"] >= 10: score += 10
    for sec in ['experience','education','project','skill','certification','achievement']:
        if sec in t: score += 7
    if re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text): score += 5
    if re.search(r'github\.com', t):  score += 5
    if re.search(r'linkedin\.com', t): score += 5
    return min(score, 100)


def _predict_roles(resume_skills: list) -> list:
    resume_set = {s.lower() for s in resume_skills}
    scores = []
    for role, req_skills in JOB_ROLES.items():
        match = len(set(req_skills) & resume_set)
        pct   = round(match / len(req_skills) * 100)
        if pct > 0:
            scores.append((role, pct))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:5]


def _suggestions(missing_skills, missing_kw, ats_score, quality_score) -> list:
    tips = []
    if ats_score < 50:
        tips.append("Your ATS score is low. Tailor your resume more closely to the job description.")
    if missing_skills:
        tips.append(f"Add these missing skills if you have them: {', '.join(missing_skills[:5])}.")
    if missing_kw:
        tips.append(f"Include these keywords from the JD: {', '.join(missing_kw[:5])}.")
    if quality_score < 50:
        tips.append("Add more sections: Projects, Certifications, or Achievements to improve quality score.")
    if ats_score >= 70:
        tips.append("Great match! Make sure your resume format is ATS-friendly (no tables/images).")
    if not tips:
        tips.append("Your resume looks great for this role. Apply with confidence!")
    return tips


def match(resume_text: str, jd_text: str) -> dict:
    r_clean = _clean(resume_text)
    j_clean = _clean(jd_text)

    # TF-IDF cosine similarity
    vec    = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf  = vec.fit_transform([r_clean, j_clean])
    sim    = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    ats    = round(sim * 100, 1)

    # Keyword analysis
    stop = {'and','or','the','a','an','in','of','to','for','with','on','at',
            'by','from','is','are','be','we','you','our','will','have','has',
            'that','this','as','it','not','but','they','their','which','who'}
    jd_kw      = {w for w in j_clean.split() if len(w) > 3 and w not in stop}
    resume_kw  = set(r_clean.split())
    matched_kw = sorted(jd_kw & resume_kw)
    missing_kw = sorted(jd_kw - resume_kw)

    # Skill gap
    r_skills = extract_skills(resume_text)
    j_skills = extract_skills(jd_text)
    matched_skills = sorted(set(r_skills["all_skills"]) & set(j_skills["all_skills"]))
    missing_skills = sorted(set(j_skills["all_skills"]) - set(r_skills["all_skills"]))

    quality = _quality_score(resume_text, r_skills)

    if ats >= 80:   label, color = "Excellent Match", "#16A34A"
    elif ats >= 60: label, color = "Good Match",      "#D97706"
    elif ats >= 40: label, color = "Average Match",   "#EA580C"
    else:           label, color = "Poor Match",      "#DC2626"

    kw_pct = round(len(matched_kw) / max(len(jd_kw), 1) * 100, 1)

    return {
        "ats_score":        ats,
        "quality_score":    quality,
        "label":            label,
        "color":            color,
        "matched_keywords": matched_kw[:25],
        "missing_keywords": missing_kw[:25],
        "matched_skills":   matched_skills,
        "missing_skills":   missing_skills,
        "resume_skills":    r_skills,
        "jd_skills":        j_skills,
        "keyword_match_pct": kw_pct,
        "suggested_roles":  _predict_roles(r_skills["all_skills"]),
        "suggestions":      _suggestions(missing_skills, missing_kw[:5], ats, quality),
    }
