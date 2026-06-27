# =============================================================================
# config.py
# =============================================================================
import os

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR  = os.path.join(BASE_DIR, "uploads")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DB_PATH     = os.path.join(BASE_DIR, "database", "resumeai.db")

for d in [UPLOAD_DIR, REPORTS_DIR, os.path.join(BASE_DIR, "database")]:
    os.makedirs(d, exist_ok=True)

APP_VERSION = "1.0.0"

PROGRAMMING_LANGUAGES = [
    "python","java","javascript","typescript","c++","c#","c","r","go","rust",
    "swift","kotlin","php","ruby","scala","perl","matlab","bash","dart","html","css","sql",
]
FRAMEWORKS_LIBRARIES = [
    "django","flask","fastapi","spring","springboot","react","reactjs","angular",
    "vuejs","nodejs","express","nextjs","tensorflow","keras","pytorch","scikit-learn",
    "sklearn","pandas","numpy","matplotlib","seaborn","plotly","opencv","nltk","spacy",
    "bootstrap","tailwind","jquery","redux","hibernate","pytest","selenium",
]
DATABASES = [
    "mysql","postgresql","postgres","sqlite","mongodb","redis","cassandra",
    "oracle","dynamodb","firebase","elasticsearch","sql server","mssql",
]
CLOUD_DEVOPS = [
    "aws","azure","gcp","google cloud","docker","kubernetes","jenkins",
    "github actions","terraform","ansible","linux","ci/cd","devops","heroku","vercel",
]
TOOLS_OTHER = [
    "git","github","gitlab","jira","postman","swagger","figma","tableau",
    "power bi","jupyter","hadoop","spark","kafka","airflow","rest api",
    "restful","microservices","agile","scrum","mlflow",
]
ALL_SKILLS = PROGRAMMING_LANGUAGES + FRAMEWORKS_LIBRARIES + DATABASES + CLOUD_DEVOPS + TOOLS_OTHER

JOB_ROLES = {
    "Python Developer":            ["python","django","flask","sql","git","rest api","pandas"],
    "Machine Learning Engineer":   ["python","tensorflow","pytorch","scikit-learn","pandas","numpy","mlflow"],
    "Data Scientist":              ["python","r","pandas","numpy","scikit-learn","matplotlib","sql","jupyter"],
    "Data Analyst":                ["sql","python","excel","pandas","tableau","power bi","matplotlib"],
    "Frontend Developer":          ["html","css","javascript","react","angular","typescript","git"],
    "Backend Developer":           ["python","java","nodejs","django","sql","postgresql","docker","git"],
    "Full Stack Developer":        ["html","css","javascript","react","nodejs","python","sql","docker"],
    "DevOps Engineer":             ["docker","kubernetes","jenkins","aws","linux","bash","terraform","ci/cd"],
    "Cloud Engineer":              ["aws","azure","gcp","terraform","docker","kubernetes","linux","python"],
    "Android Developer":           ["kotlin","java","firebase","git","rest api","sql"],
}
