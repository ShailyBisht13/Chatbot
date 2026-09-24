# language_engine.py — SAFE & FAIL-PROOF

import os
import csv
import re

BASE = os.path.join(os.path.dirname(__file__), "datasets", "regional")


def load_csv_sentences(filename):
    path = os.path.join(BASE, filename)
    data = []

    if not os.path.exists(path):
        print(f"⚠️ Dataset missing: {filename} — skipping load")
        return data

    try:
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0].strip():
                    data.append(row[0])
    except Exception as e:
        print(f"⚠️ Failed to load {filename}: {e}")

    return data


# ✅ SAFE LOAD (EMPTY LIST IF FILE MISSING)
KUMAONI_DATA = load_csv_sentences("kumaoni_full_5000.csv")
GARHWALI_DATA = load_csv_sentences("garhwali_full_5000.csv")


def detect_language(text: str):
    t = (text or "").lower()

    if re.search(r"[অ-হ]", t):
        return "bn"

    if re.search(r"[अ-ह]", t):
        return "hi"

    if any(w in t for w in ["मी", "आहे", "प्रवास", "हवामान"]):
        return "mr"

    return "en"


def get_regional_response(lang, fallback_text):
    if lang == "kumaoni" and KUMAONI_DATA:
        return KUMAONI_DATA[0]

    if lang == "garhwali" and GARHWALI_DATA:
        return GARHWALI_DATA[0]

    return fallback_text
