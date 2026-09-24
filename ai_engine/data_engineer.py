# data_engineer.py — FINAL REGIONAL ENGINE (UPDATED & SAFE) ✅

import csv
import os

# -------------------------------------------------
# DATASET PATHS
# -------------------------------------------------
BASE_DIR = os.path.dirname(__file__)

KUMAONI_CSV = os.path.join(BASE_DIR, "kumaoni_full_5000.csv")
GARHWALI_CSV = os.path.join(BASE_DIR, "garhwali_full_5000.csv")

# -------------------------------------------------
# SIMPLE TEXT CLEAN
# -------------------------------------------------
def clean(text):
    return (text or "").lower().strip()

# -------------------------------------------------
# LOAD CSV ONCE (FAST)
# -------------------------------------------------
_kum_cache = None
_gar_cache = None

def _load_csv(path):
    data = []
    if not os.path.exists(path):
        return data

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                "q": clean(row.get("question") or row.get("query")),
                "a": row.get("answer", "")
            })
    return data

def _init_cache():
    global _kum_cache, _gar_cache
    if _kum_cache is None:
        _kum_cache = _load_csv(KUMAONI_CSV)
    if _gar_cache is None:
        _gar_cache = _load_csv(GARHWALI_CSV)

# -------------------------------------------------
# 🧠 AUTO-DETECT REGIONAL LANGUAGE
# -------------------------------------------------
def detect_regional_language(text: str):
    """
    Very light heuristic:
    - Defaults to Kumaoni
    - Switches to Garhwali if typical patterns found
    """
    t = clean(text)

    garhwali_markers = ["छौं", "छौ", "कु", "कौं", "थ्यो"]
    kumaoni_markers = ["छ", "छौ", "कैं", "हैं"]

    if any(m in t for m in garhwali_markers):
        return "gar"

    return "kum"

# -------------------------------------------------
# 🔑 MAIN FUNCTION (BACKWARD COMPATIBLE)
# -------------------------------------------------
def fetch_regional_answer(user_input: str, language: str = None):
    """
    Fetches Kumaoni / Garhwali answers from CSV.
    - Auto-detects language if not provided
    - Safe fallback if no match found
    """

    _init_cache()
    q = clean(user_input)

    if not q:
        return None

    # Auto-detect if language not explicitly given
    if language is None:
        language = detect_regional_language(q)

    dataset = _kum_cache if language == "kum" else _gar_cache

    # Exact / substring match
    for row in dataset:
        if row["q"] and row["q"] in q:
            return row["a"]

    # Keyword-level fallback
    for row in dataset:
        if row["q"] and any(word in q for word in row["q"].split()):
            return row["a"]

    # Final fallback (regional)
    return (
        "माफ़ करौ, इ सवाल का जवाब अभी डेटाबेस म न्है छ।"
        if language == "kum"
        else "माफ करियौ, इ सवाल का जवाब अभी डेटाबेस म न्है छ।"
    )
