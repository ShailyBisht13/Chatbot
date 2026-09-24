# crowd_prediction.py (very simple seasonal predictor)
import pandas as pd
import numpy as np
from datetime import datetime

# load historical month counts if available
def predict_crowd(place_name, month=None):
    # if dataset exists use heuristics, else fallback
    if month is None:
        month = datetime.now().month
    # simple rule: pilgrimage sites peak in Apr-Jun and Sep-Nov
    if place_name.lower() in ["kedarnath","badrinath","haridwar","rishikesh"]:
        if month in [4,5,6,9,10,11]:
            return "High"
    return "Low"
