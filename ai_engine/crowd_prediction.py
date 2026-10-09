# crowd_prediction.py — seasonal HEURISTIC (not machine learning)
from datetime import datetime

# Char Dham shrines close for winter (roughly Nov-Apr); dates vary each year.
CHAR_DHAM = {"kedarnath", "badrinath", "gangotri", "yamunotri"}
GANGA_TOWNS = {"haridwar", "rishikesh"}
CHAR_DHAM_CLOSED = {11, 12, 1, 2, 3}


def predict_crowd(place_name, month=None):
    """Return 'High' / 'Moderate' / 'Low' / 'Closed (winter)', or None if we have no rule
    for the place (so the caller shows nothing instead of a misleading 'Low')."""
    month = month or datetime.now().month
    place = (place_name or "").strip().lower()

    if place in CHAR_DHAM:
        if month in CHAR_DHAM_CLOSED:
            return "Closed (winter)"
        if month in (5, 6, 9, 10):
            return "High"
        return "Moderate"          # April (season opening) and monsoon months

    if place in GANGA_TOWNS:
        return "High" if month in (4, 5, 6, 9, 10, 11) else "Moderate"

    return None