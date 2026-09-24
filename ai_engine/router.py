# =========================================================
# router.py — FULLY WORKING MULTIFUNCTIONAL AI ROUTER
# =========================================================
import requests
import re
import os
import json
from typing import Optional

from intent_classifier import classify_intent
from llm_engine import run_llm
from tourism_rag import answer_tourism_rag
from spiritual_rag import answer_spiritual_rag
from monuments_ai import recognize_monument
from persona_manager import get_persona
from crowd_prediction import predict_crowd

# Optional modules
try:
    from voice_output import generate_tts_audio
except Exception:
    generate_tts_audio = None

try:
    from meditation_engine import generate_meditation_audio
except Exception:
    generate_meditation_audio = None

# =========================================================
# 🔑 API KEYS & CONFIG
# =========================================================
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

LANG_MAP = {
    "en": {"name": "English", "tts": "en"},
    "hi": {"name": "Hindi", "tts": "hi"},
    "sa": {"name": "Sanskrit", "tts": "hi"},
    "mr": {"name": "Marathi", "tts": "mr"},
    "bn": {"name": "Bengali", "tts": "bn"},
}

def shiva_intro(lang="en"):
    return {
        "hi": "मैं SHIVA BOT हूँ — आपका पर्यटन एवं आध्यात्मिक सहायक।\n\n",
        "sa": "अहं SHIVA BOT अस्मि — तव पर्यटन–आध्यात्मिक सहायकः।\n\n",
        "mr": "मी SHIVA BOT आहे — तुमचा पर्यटन व आध्यात्मिक सहाय्यक.\n\n",
        "bn": "আমি SHIVA BOT — আপনার পর্যটন ও আধ্যাত্মিক সহকারী।\n\n",
    }.get(lang, "I am SHIVA BOT — your Tourism & Spiritual assistant.\n\n")

# Extract city name cleanly from weather query
def extract_city(query):
    # Pattern 1: Look for "weather in/of/for/at/near <city>"
    m = re.search(r"(?i)\bweather\s+(?:in|of|for|at|near|around)\s+([a-z\s]+)", query)
    if m:
        city = m.group(1)
        city = re.sub(r"(?i)\b(today|now|right|current|forecast|please)\b", "", city).strip()
        if city:
            return city.title()

    # Pattern 2: Look for "<city> weather"
    m = re.search(r"(?i)\b([a-z\s]+)\s+weather\b", query)
    if m:
        city = m.group(1)
        city = re.sub(r"(?i)\b(can|you|please|tell|me|what|is|the|how|show|give|check)\b", "", city).strip()
        if city:
            return city.title()

    # Fallback: remove common conversational stop-words
    stop_words = r"(?i)\b(can|you|please|tell|me|what|is|the|a|an|weather|like|in|of|for|at|near|around|current|forecast|today|how|show|give|check|temperature|condition|status|right|now)\b"
    cleaned = re.sub(stop_words, " ", query)
    cleaned = re.sub(r"[?\!.,]", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned.title() if cleaned else "Rishikesh"

# =========================================================
# 🧘 MEDITATION LOGIC (INTERACTIVE)
# =========================================================
def handle_meditation(lang, query):
    q = query.lower()
    
    choice = None
    if "forest" in q or "जंगल" in q: choice = "forest"
    elif "river" in q or "नदी" in q: choice = "river"
    elif "wind" in q or "हवा" in q: choice = "wind"
    elif "rain" in q or "बारिश" in q: choice = "rain"

    if choice:
        if generate_meditation_audio:
            med_result = generate_meditation_audio(language=lang, ambience=choice, duration_sec=60)
            if med_result.get("status") == "ok":
                msgs = {
                    "en": f"🧘 Starting 1-minute meditation with {choice.title()} ambient sound. Take a deep breath, close your eyes, and relax...",
                    "hi": f"🧘 {choice} की शांत ध्वनि के साथ 1 मिनट का ध्यान शुरू हो रहा है। लंबी सांस लें और शांत रहें...",
                    "bn": f"🧘 {choice} এর শান্ত শব্দসহ ১ মিনিটের ধ্যান শুরু হচ্ছে। গভীর শ্বাস নিন এবং শান্ত থাকুন...",
                    "mr": f"🧘 {choice} च्या शांत ध्वनीसह १ मिनिटाचे ध्यान सुरू होत आहे. शांत राहा..."
                }
                reply = msgs.get(lang, msgs["en"])
                return {"answer": reply, "audio_url": med_result.get("audio_url")}
            else:
                return f"Meditation error: {med_result.get('message')}"
        else:
            return "Meditation service currently unavailable."

    questions = {
        "en": "🧘 Which ambient sound would you like for your 1-minute meditation?\n• Forest (Trees & birds)\n• River (Flowing Ganga water)\n• Wind (Highland breeze)\n• Rain (Gentle rainfall)",
        "hi": "🧘 ध्यान के लिए आप कौन सी ध्वनि पसंद करेंगे?\n• जंगल (Forest)\n• नदी (River)\n• हवा (Wind)\n• बारिश (Rain)",
        "bn": "🧘 ধ্যানের জন্য আপনি কোন শব্দটি পছন্দ করবেন?\n• বন (Forest)\n• নদী (River)\n• বাতাস (Wind)\n• বৃষ্টি (Rain)",
        "mr": "🧘 ध्यानासाठी तुम्हाला कोणता आवाज आवडेल?\n• जंगल (Forest)\n• नदी (River)\n• वारा (Wind)\n• पाऊस (Rain)"
    }
    return questions.get(lang, questions["en"])

# =========================================================
# 🚦 MAIN ROUTER
# =========================================================
def ai_router(
    user_input: str,
    lang: str = "en",
    persona: str = "travel_guide",
    image_path: Optional[str] = None
):
    lang = lang if lang in LANG_MAP else "en"
    intent = classify_intent(user_input)
    q = user_input.lower()
    persona_prompt = get_persona(persona)
    lang_name = LANG_MAP[lang]["name"]

    # ---------- AUTOMATIC IMAGE ATTACHMENT OVERRIDE ----------
    # If a valid image file exists, evaluate it directly (Monument location or Yoga evaluation)
    if image_path and os.path.isfile(image_path):
        if intent == "yoga" or "yoga" in q or "pose" in q or "asana" in q:
            prompt = f"Analyze this yoga posture image. Provide:\n1. Asana Name & Sanskrit Origin\n2. Step-by-Step Alignment Tips\n3. Health & Spiritual Benefits\n4. Precautions.\nReply ONLY in {lang_name}."
            raw_ans = run_llm(prompt, f"User uploaded a yoga pose image for evaluation.")
            result = {"status": "ok", "intent": "yoga", "answer": f"🧘 Yoga Pose Evaluation:\n\n{raw_ans}", "lang": lang}
        else:
            mon_res = recognize_monument(image_path)
            if isinstance(mon_res, dict) and "monument" in mon_res:
                name = mon_res["monument"]
                location = mon_res.get("location", "India")
                conf = mon_res["confidence"]
                prompt = f"You identified the monument '{name}' located at '{location}' with {conf}% confidence.\nState clearly WHERE it is located (City, State, Country).\nInclude:\n1. Exact Location: {location}\n2. Architectural & Historical Highlights\n3. Spiritual/Cultural Significance\n4. Best Time to Visit & Visitor Tips.\nReply ONLY in {lang_name}."
                details = run_llm(prompt, f"Tell me about {name} located at {location}.")
                formatted = f"🏛 Monument Identified: **{name}** ({conf}% Confidence)\n📍 Location: **{location}**\n\n{details}"
                result = {"status": "ok", "intent": "monument", "answer": formatted, "lang": lang}
            else:
                result = {"status": "ok", "intent": "monument", "answer": "Could not recognize monument from the uploaded image.", "lang": lang}

        if generate_tts_audio and isinstance(result.get("answer"), str):
            tts_lang = LANG_MAP[lang]["tts"] or "en"
            audio_url = generate_tts_audio(result["answer"], lang=tts_lang)
            if audio_url:
                result["audio_url"] = audio_url

        return result

    # ---------- TOILET / WASHROOM OVERRIDE ----------
    if any(x in q for x in ["toilet", "washroom", "bathroom", "शौचालय", "स्वच्छतागृह", "টয়লেট"]):
        if "sudhowala" in q or "सुधोवाला" in q:
            reply = "🚻 Public restrooms near Sudhowala:\n1. Sudhowala Bus Stop / Main Road Complex\n2. Near Prem Nagar Market & Uttaranchal University vicinity\n3. ISBT Dehradun Public Toilet Complex."
        elif "dehradun" in q or "देहरादून" in q or "clock tower" in q:
            reply = "🚻 Public restrooms in Dehradun:\n1. Clock Tower Public Toilet Complex (Paltan Bazaar entrance)\n2. Dehradun Railway Station & Parade Ground\n3. ISBT Dehradun Main Terminal."
        elif "kedarnath" in q or "केदारनाथ" in q:
            reply = "🚻 Public restrooms in Kedarnath:\n1. Gaurikund Base Camp & Trekking Route Points\n2. Lincholi & Bheembali Halt Points\n3. Kedarnath Temple Outer Complex."
        elif "rishikesh" in q or "ऋषिकेश" in q:
            reply = "🚻 Public restrooms in Rishikesh:\n1. Main Bus Stand & GMVN Rest House\n2. Near Laxman Jhula & Ram Jhula entrances\n3. Triveni Ghat Promenade."
        else:
            loc = extract_city(user_input)
            prompt = f"Provide public restroom / toilet location guidance for tourists in '{loc}'. State 3 clear public locations. Reply ONLY in {lang_name}."
            reply = run_llm(prompt, user_input)
        return {"status": "ok", "intent": "toilet", "answer": reply, "lang": lang}

    # ---------- WEATHER ----------
    if "weather" in q or "मौसम" in q or "हवामान" in q or "আবহাওয়া" in q:
        place = extract_city(user_input)
        try:
            r = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": place, "appid": OPENWEATHER_API_KEY, "units": "metric"},
                timeout=6
            )
            if r.status_code == 200:
                d = r.json()
                temp = d["main"]["temp"]
                feels_like = d["main"]["feels_like"]
                desc = d["weather"][0]["description"].title()
                humidity = d["main"]["humidity"]
                wind_spd = d["wind"]["speed"]
                city_name = d.get("name", place.title())
                country = d.get("sys", {}).get("country", "IN")
                
                weather_info = f"🌦 Current Weather in **{city_name}, {country}**:\n• Temperature: {temp}°C (Feels like {feels_like}°C)\n• Conditions: {desc}\n• Humidity: {humidity}%\n• Wind Speed: {wind_spd} m/s"
                
                crowd_info = predict_crowd(city_name)
                if crowd_info:
                    weather_info += f"\n• Estimated Visitor Traffic: {crowd_info} Level"
                    
                result = {"status": "ok", "intent": "weather", "answer": weather_info, "lang": lang}
            else:
                result = {"status": "ok", "intent": "weather", "answer": f"Could not find live weather for '{place}'. Please specify a major city or town name.", "lang": lang}
        except Exception as e:
            result = {"status": "ok", "intent": "weather", "answer": f"Weather service error: {str(e)}", "lang": lang}

    # ---------- MEDITATION ----------
    elif intent == "meditation" or any(x in q for x in ["forest", "river", "wind", "rain"]):
        med_res = handle_meditation(lang, user_input)
        if isinstance(med_res, dict):
            answer = med_res.get("answer", "")
            audio_url = med_res.get("audio_url")
        else:
            answer = med_res
            audio_url = None

        result = {
            "status": "ok",
            "intent": "meditation",
            "answer": answer,
            "audio_url": audio_url,
            "lang": lang
        }

    # ---------- YOGA ----------
    elif intent == "yoga":
        prompt = f"{persona_prompt}\nYou are an expert Yoga instructor. Recommend top yoga postures (Asanas) with step-by-step instructions, breathing guidance (Pranayama), health benefits, and precautions. Reply ONLY in {lang_name}."
        yoga_ans = run_llm(prompt, user_input)
        result = {"status": "ok", "intent": "yoga", "answer": yoga_ans, "lang": lang}

    # ---------- MONUMENT ----------
    elif intent == "monument":
        prompt = f"{persona_prompt}\nProvide detailed historical, architectural, and pilgrimage information about monuments and temples. Reply ONLY in {lang_name}."
        mon_ans = run_llm(prompt, user_input)
        result = {"status": "ok", "intent": "monument", "answer": mon_ans, "lang": lang}

    # ---------- SPIRITUAL ----------
    elif intent == "spiritual":
        rag_ans = answer_spiritual_rag(user_input, lang=lang)
        result = {"status": "ok", "intent": "spiritual", "answer": shiva_intro(lang) + rag_ans, "lang": lang}

    # ---------- TOURISM ----------
    elif intent == "tourism":
        rag_ans = answer_tourism_rag(user_input, lang=lang)
        result = {"status": "ok", "intent": "tourism", "answer": shiva_intro(lang) + rag_ans, "lang": lang}

    # ---------- GENERAL FALLBACK ----------
    else:
        system = f"{persona_prompt}\nSTRICT RULE:\n- Answer ONLY in {lang_name}\n- Use clear headings, separate lines, and bullet points for readability."
        final = shiva_intro(lang) + run_llm(system, user_input)
        result = {"status": "ok", "intent": "general", "answer": final, "lang": lang}

    # ---------- SERVER-SIDE TTS GENERATION ----------
    if generate_tts_audio and isinstance(result.get("answer"), str) and result.get("intent") != "meditation":
        tts_lang = LANG_MAP[lang]["tts"] or "en"
        audio_url = generate_tts_audio(result["answer"], lang=tts_lang)
        if audio_url:
            result["audio_url"] = audio_url

    return result
