# intent_classifier.py — multilingual, word-boundary safe
import re


def contains_any(text: str, keywords) -> bool:
    """
    ASCII keywords are matched as WHOLE words ('pose' no longer matches 'purpose',
    'rain' no longer matches 'train'). Non-ASCII (Hindi/Bengali/Marathi) keywords use
    substring matching, because Python's \\b breaks on Indic combining marks (matras).
    """
    t = (text or "").lower()
    for kw in keywords:
        kw = kw.lower()
        if kw.isascii():
            if re.search(rf"(?<![a-z0-9]){re.escape(kw)}(?![a-z0-9])", t):
                return True
        elif kw in t:
            return True
    return False


MEDITATION = ["meditation", "meditate", "meditating", "mindfulness",
              "ध्यान", "ধ্যান"]
YOGA = ["yoga", "asana", "asanas", "pose", "poses", "pranayama",
        "योग", "आसन", "যোগ", "যোগাসন"]
MONUMENT = ["monument", "monuments", "identify", "heritage",
            "स्मारक", "इमारत", "স্মৃতিস্তম্ভ"]

# Location / travel-utility questions. Checked BEFORE spiritual so that
# "Where is Kedarnath Temple?" is tourism, not spiritual.
TOURISM_STRONG = [
    "where is", "where's", "located", "location", "how to reach", "route", "routes",
    "weather", "crowd", "washroom", "toilet", "bathroom", "hotel", "hotels",
    "trek", "treks", "trekking", "travel", "trip", "trips", "tour", "tours",
    "कहाँ", "स्थित", "मौसम", "भीड़", "शौचालय", "टॉयलेट", "होटल", "यात्रा", "घूमने",
    "कुठे", "हवामान", "गर्दी", "स्वच्छतागृह", "हॉटेल", "प्रवास",
    "কোথায়", "আবহাওয়া", "ভিড়", "শৌচালয়", "টয়লেট", "হোটেল", "ভ্রমণ",
]

SPIRITUAL = ["gita", "shloka", "shlokas", "spiritual", "significance", "temple", "temples",
             "mandir", "mantra", "puja",
             "गीता", "श्लोक", "मंदिर", "मन्दिर", "मंत्र",
             "মন্দির", "গীতা"]

TOURISM_WEAK = ["visit", "visiting", "stay", "place", "places", "hill station", "district",
                "attraction", "attractions", "mountain", "mountains",
                "स्थान", "जिला", "पहाड़", "ठिकाण", "স্থান"]


def classify_intent(text: str) -> str:
    """Priority order: meditation > yoga > monument > tourism(strong) > spiritual > tourism(weak) > general"""
    if contains_any(text, MEDITATION):
        return "meditation"
    if contains_any(text, YOGA):
        return "yoga"
    if contains_any(text, MONUMENT):
        return "monument"
    if contains_any(text, TOURISM_STRONG):
        return "tourism"
    if contains_any(text, SPIRITUAL):
        return "spiritual"
    if contains_any(text, TOURISM_WEAK):
        return "tourism"
    return "general"   # removed the unused 'data_engineer' intent