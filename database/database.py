# =============================================================================
# database/database.py — SQLite History Store
# =============================================================================
import sqlite3, json
from datetime import datetime
from config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name  TEXT,
            resume_filename TEXT,
            ats_score       REAL,
            quality_score   REAL,
            label           TEXT,
            matched_skills  TEXT,
            missing_skills  TEXT,
            suggested_roles TEXT,
            analyzed_at     TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_analysis(parsed: dict, result: dict):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO analyses
        (candidate_name, resume_filename, ats_score, quality_score,
         label, matched_skills, missing_skills, suggested_roles, analyzed_at)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        parsed.get("name", "Unknown"),
        parsed.get("filename", "resume"),
        result.get("ats_score", 0),
        result.get("quality_score", 0),
        result.get("label", ""),
        json.dumps(result.get("matched_skills", [])),
        json.dumps(result.get("missing_skills", [])),
        json.dumps([r[0] for r in result.get("suggested_roles", [])]),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ))
    conn.commit()
    conn.close()


def get_all_analyses():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM analyses ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows


def delete_analysis(row_id: int):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM analyses WHERE id=?", (row_id,))
    conn.commit()
    conn.close()


def clear_all():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM analyses")
    conn.commit()
    conn.close()
