# intent_classifier.py — MULTILINGUAL & ROBUST (UPDATED, SAFE)

def classify_intent(text: str):
    t = (text or "").lower()

    # ---------------------------------
    # 🧘 Meditation (CHECK FIRST)
    # ---------------------------------
    if any(x in t for x in [
        "meditation", "meditate", "mindfulness",
        "ध्यान", "ध्यान करना",
        "ধ্যান"
    ]):
        return "meditation"

    # ---------------------------------
    # 🧘 Yoga
    # ---------------------------------
    if any(x in t for x in [
        "yoga", "asana", "pose",
        "योग", "आसन",
        "যোগ", "যোগাসন"
    ]):
        return "yoga"

    # ---------------------------------
    # 🏛 Monument / Image
    # ---------------------------------
    if any(x in t for x in [
        "monument", "identify", "heritage",
        "स्मारक", "इमारत",
        "স্মৃতিস্তম্ভ"
    ]):
        return "monument"

    # ---------------------------------
    # 🕉 Spiritual
    # ---------------------------------
    if any(x in t for x in [
        "gita", "shloka", "spiritual", "significance",
        "temple", "mandir",
        "गीता", "श्लोक", "मंदिर",
        "মন্দির"
    ]):
        return "spiritual"

    # ---------------------------------
    # 🌍 Tourism + Utilities
    # ---------------------------------
    if any(x in t for x in [
        # English
        "travel", "tour", "trip", "visit", "hotel", "stay",
        "weather", "crowd", "washroom", "toilet", "bathroom",
        "trek", "route", "located", "location", "where is", "where's",
        "place", "places", "hill station", "district", "attraction", "mount",

        # Hindi
        "यात्रा", "घूमने", "होटल", "मौसम", "भीड़",
        "शौचालय", "टॉयलेट", "कहाँ", "स्थान", "स्थित", "जिला", "पहाड़",

        # Marathi
        "प्रवास", "हॉटेल", "हवामान", "गर्दी",
        "शौचालय", "स्वच्छतागृह", "कुठे", "ठिकाण",

        # Bengali
        "ভ্রমণ", "হোটেল", "আবহাওয়া", "ভিড়",
        "শৌচালয়", "টয়লেট", "কোথায়", "স্থান"
    ]):
        return "tourism"

    # ---------------------------------
    # 🧠 Data Engineer
    # ---------------------------------
    if any(x in t for x in [
        "dataset", "data", "csv", "etl",
        "डेटा", "डाटासेट"
    ]):
        return "data_engineer"

    # ---------------------------------
    # Default
    # ---------------------------------
    return "general"
