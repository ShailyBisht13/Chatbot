# dataset_loader.py — FINAL WORKING VERSION
import json, csv, os

BASE = os.path.join(os.path.dirname(__file__), "datasets")

# ---------------------------------------------------------
# INTERNAL JSON PARSER (supports numbered / JSONL formats)
# ---------------------------------------------------------
def _read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()

        # Case 1: Normal JSON array
        if text.startswith("["):
            return json.loads(text)

        # Case 2: JSONL or numbered entries (1: {...})
        items = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            # Try normal JSON first
            try:
                items.append(json.loads(line))
                continue
            except:
                pass

            # Handle "1: { ... }"
            if ":" in line:
                try:
                    line = line.split(":", 1)[1].strip()
                    items.append(json.loads(line))
                except:
                    pass

        return items


# ---------------------------------------------------------
# 1️⃣ TOURISM DATA LOADERS
# ---------------------------------------------------------
def load_tourism_data():
    p_json = os.path.join(BASE, "tourism", "Expanded_Indian_Travel_Dataset.json")
    if os.path.exists(p_json):
        return _read_json(p_json)

    p_csv = os.path.join(BASE, "tourism", "Expanded_Indian_Travel_Dataset.csv")
    if os.path.exists(p_csv):
        rows = []
        with open(p_csv, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rows.append(row)
        return rows

    return []


# ---------------------------------------------------------
# 2️⃣ SPIRITUAL DATA LOADERS
# ---------------------------------------------------------
def load_spiritual_data():
    p = os.path.join(BASE, "spiritual", "bhagwad_gita.csv")
    if os.path.exists(p):
        rows = []
        with open(p, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rows.append(row)
        return rows
    return []


def load_temples():
    """REQUIRED by spiritual_rag.py — Merges temples.json and temples_v2.json for comprehensive coverage"""
    results = {}
    
    # 1. Load temples.json
    p1 = os.path.join(BASE, "spiritual", "temples.json")
    if os.path.exists(p1):
        try:
            with open(p1, encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    results.update(data)
        except Exception:
            pass

    # 2. Load temples_v2.json
    p2 = os.path.join(BASE, "spiritual", "temples_v2.json")
    if os.path.exists(p2):
        try:
            with open(p2, encoding="utf-8") as f:
                data2 = json.load(f)
                if isinstance(data2, list):
                    for item in data2:
                        name = item.get("name_en") or item.get("id") or "Temple"
                        # Clean up representative placeholders if any
                        if "representative" in name.lower() or "example" in name.lower():
                            continue
                        results[name] = {
                            "origin_story": item.get("origin_story_en", ""),
                            "significance": item.get("significance_en", ""),
                            "rituals_festivals": f"{item.get('rituals_en', '')} | Festivals: {item.get('festivals_en', '')}",
                            "best_time_to_visit": item.get("best_time_en", ""),
                            "spiritual_meaning": item.get("spiritual_meaning_en", ""),
                            "location": f"{item.get('location_brief_en', '')}, {item.get('state', '')}",
                            "shloka": item.get("shloka_sanskrit", "")
                        }
        except Exception:
            pass

    return results


def load_shlokas():
    p = os.path.join(BASE, "spiritual", "shlokas.json")
    if os.path.exists(p):
        return json.load(open(p, encoding="utf-8"))
    return {}


# ---------------------------------------------------------
# 3️⃣ YOGA DATA
# ---------------------------------------------------------
def load_yoga_train():
    p = os.path.join(BASE, "yoga", "yoga_train.txt")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []


# ---------------------------------------------------------
# 4️⃣ MONUMENTS METADATA
# ---------------------------------------------------------
def load_monuments_meta():
    p = os.path.join(BASE, "monuments", "monuments_list.json")
    if os.path.exists(p):
        return json.load(open(p, encoding="utf-8"))
    return []
