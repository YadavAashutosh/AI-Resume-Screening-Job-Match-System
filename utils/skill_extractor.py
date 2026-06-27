# =============================================================================
# utils/skill_extractor.py
# =============================================================================
import re
from config import (PROGRAMMING_LANGUAGES, FRAMEWORKS_LIBRARIES,
                    DATABASES, CLOUD_DEVOPS, TOOLS_OTHER)


def _find(skill_list, text_lower):
    found = []
    for skill in skill_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill.upper() if len(skill) <= 3 else skill.title())
    return sorted(set(found))


def extract_skills(text: str) -> dict:
    t = text.lower()
    langs  = _find(PROGRAMMING_LANGUAGES, t)
    fworks = _find(FRAMEWORKS_LIBRARIES, t)
    dbs    = _find(DATABASES, t)
    cloud  = _find(CLOUD_DEVOPS, t)
    tools  = _find(TOOLS_OTHER, t)
    all_s  = langs + fworks + dbs + cloud + tools
    return {
        "programming_languages": langs,
        "frameworks":  fworks,
        "databases":   dbs,
        "cloud_devops": cloud,
        "tools":       tools,
        "all_skills":  all_s,
        "total_count": len(all_s),
    }
