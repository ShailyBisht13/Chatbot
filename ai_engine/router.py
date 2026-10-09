# =========================================================
# router.py — Multifunctional AI Router with OpenWeather, Hotel API & Gemini Fallback
# =========================================================
import os
import re
import logging
from typing import Optional

from intent_classifier import classify_intent, contains_any
from llm_engine import run_llm, run_vision_llm, is_llm_error
from languages import LANG_MAP, lang_name
from tourism_rag import answer_tourism_rag
from spiritual_rag import answer_spiritual_rag
from monuments_ai import recognize_monument
from persona_manager import get_persona
from crowd_prediction import predict_crowd
from realtime_services import get_live_weather, get_hotel_recommendations, get_live_crowd

logger = logging.getLogger(__name__)

try:
    from voice_output import generate_tts_audio
except Exception:
    generate_tts_audio = None
try:
    from meditation_engine import generate_meditation_audio
except Exception:
    generate_meditation_audio = None


def shiva_intro(lang="en"):
    return {
        "hi": "मैं SHIVA BOT हूँ — आपका पर्यटन एवं आध्यात्मिक सहायक।\n\n",
        "sa": "अहं SHIVA BOT अस्मि — तव पर्यटन–आध्यात्मिक सहायकः।\n\n",
        "mr": "मी SHIVA BOT आहे — तुमचा पर्यटन व आध्यात्मिक सहाय्यक.\n\n",
        "bn": "আমি SHIVA BOT — আপনার পর্যটন ও আধ্যাত্মিক সহকারী।\n\n",
    }.get(lang, "I am SHIVA BOT — your Tourism & Spiritual assistant.\n\n")


def _with_intro(answer, lang):
    """Don't prepend the greeting to error messages."""
    return answer if is_llm_error(answer) else shiva_intro(lang) + answer


# ---------------------------------------------------------
# City extraction
# ---------------------------------------------------------
_NOISE = (
    r"can|could|you|please|tell|me|what|whats|what's|is|are|the|a|an|weather|like|in|of|for|at|"
    r"near|around|nearby|current|currently|forecast|today|tomorrow|tonight|now|right|how|show|"
    r"give|check|temperature|condition|status|toilet|toilets|washroom|bathroom|restroom|public|"
    r"hotel|hotels|homestay|homestays|resort|resorts|lodge|stay|stays|accommodation|where|find|"
    r"i|need|want|to|know|about|recommend|best|good|cheap|budget"
)


def _clean_city(text):
    text = re.sub(rf"(?i)\b({_NOISE})\b", " ", text)
    text = re.sub(r"[?!.,]", " ", text)
    return re.sub(r"\s+", " ", text).strip().title()


def extract_city(query, default="Rishikesh"):
    m = (
        re.search(r"(?i)\b(?:weather|hotel|hotels|homestay|stay|resort|toilet|restroom)\s+(?:in|of|for|at|near|around)\s+([a-z\s]+)", query)
        or re.search(r"(?i)\b([a-z\s]+)\s+(?:weather|hotel|hotels|homestay|stay|resort|toilet)\b", query)
    )
    city = _clean_city(m.group(1)) if m else _clean_city(query)
    return city or default


# ---------------------------------------------------------
# Meditation (stateless two-step flow)
# ---------------------------------------------------------
AMBIENCE_WORDS = {
    "forest": ["forest", "jungle", "जंगल", "বন"],
    "river": ["river", "नदी", "নদী"],
    "wind": ["wind", "breeze", "हवा", "वारा", "বাতাস"],
    "rain": ["rain", "बारिश", "पाऊस", "বৃষ্টি"],
}

MEDITATION_QUESTIONS = {
    "en": "🧘 Which ambient sound would you like for your 1-minute meditation?\n• Forest (Trees & birds)\n• River (Flowing Ganga water)\n• Wind (Highland breeze)\n• Rain (Gentle rainfall)",
    "hi": "🧘 ध्यान के लिए आप कौन सी ध्वनि पसंद करेंगे?\n• जंगल (Forest)\n• नदी (River)\n• हवा (Wind)\n• बारिश (Rain)",
    "bn": "🧘 ধ্যানের জন্য আপনি কোন শব্দটি পছন্দ করবেন?\n• বন (Forest)\n• নদী (River)\n• বাতাস (Wind)\n• বৃষ্টি (Rain)",
    "mr": "🧘 ध्यानासाठी तुम्हाला कोणता आवाज आवडेल?\n• जंगल (Forest)\n• नदी (River)\n• वारा (Wind)\n• पाऊस (Rain)",
}
MEDITATION_STARTING = {
    "en": "🧘 Starting 1-minute meditation with {c} ambient sound. Take a deep breath, close your eyes, and relax...",
    "hi": "🧘 {c} की शांत ध्वनि के साथ 1 मिनट का ध्यान शुरू हो रहा है। लंबी सांस लें और शांत रहें...",
    "bn": "🧘 {c} এর শান্ত শব্দসহ ১ মিনিটের ধ্যান শুরু হচ্ছে। গভীর শ্বাস নিন এবং শান্ত থাকুন...",
    "mr": "🧘 {c} च्या शांत ध्वनीसह १ मिनिटाचे ध्यान सुरू होत आहे. शांत राहा...",
}


def _pick_ambience(query):
    for name, words in AMBIENCE_WORDS.items():
        if contains_any(query, words):
            return name
    return None


def is_meditation_reply(q, intent):
    return intent == "meditation" or (_pick_ambience(q) is not None and len(q.split()) <= 3)


def handle_meditation(lang, query):
    choice = _pick_ambience(query)
    if not choice:
        return {"answer": MEDITATION_QUESTIONS.get(lang, MEDITATION_QUESTIONS["en"]), "audio_url": None}
    if not generate_meditation_audio:
        return {"answer": "Meditation service currently unavailable.", "audio_url": None}
    res = generate_meditation_audio(ambience=choice, duration_sec=60)
    if res.get("status") != "ok":
        return {"answer": f"Meditation error: {res.get('message')}", "audio_url": None}
    msg = MEDITATION_STARTING.get(lang, MEDITATION_STARTING["en"]).format(c=choice.title())
    return {"answer": msg, "audio_url": res.get("audio_url")}


NOT_A_MONUMENT_MSG = {
    "en": "🏛️ This image does not appear to be an Indian monument or historical heritage site.",
    "hi": "🏛️ यह फोटो किसी भारतीय स्मारक या ऐतिहासिक स्थल की प्रतीत नहीं होती।",
    "sa": "🏛️ इदं चित्रं भारतीयस्मारकस्य अथवा ऐतिहासिकस्थानस्य न दृश्यते।",
    "bn": "🏛️ এই ছবিটি কোনো ভারতীয় স্মৃতিস্তম্ভ বা ঐতিহাসিক স্থানের মতো মনে হচ্ছে না।",
    "mr": "🏛️ हा फोटो कोणत्याही भारतीय स्मारकाचा किंवा ऐतिहासिक स्थळाचा दिसत नाही.",
}


def _handle_image(intent, lang, image_path):
    lname = lang_name(lang)

    # 1. If intent is explicitly yoga, or if user is asking about posture
    if intent == "yoga":
        prompt = (
            f"Analyze this yoga posture image. Provide:\n1. Asana Name & Sanskrit Origin\n"
            f"2. Step-by-Step Alignment Tips\n3. Health & Spiritual Benefits\n4. Precautions.\n"
            f"Reply ONLY in {lname}."
        )
        analysis = run_vision_llm(prompt, image_path)
        if analysis:
            answer = f"🧘 **Yoga Pose Evaluation**:\n\n{analysis}"
        else:
            answer = run_llm(
                f"{get_persona('yoga_trainer')}\nReply ONLY in {lname}. Give tips for common asanas with alignment, breathing and precautions.",
                "The user uploaded a yoga pose photo for evaluation.",
            )
        return {"status": "ok", "intent": "yoga", "answer": answer, "lang": lang}

    # 2. Check if the image is a monument
    mon = recognize_monument(image_path)
    if mon.get("is_monument"):
        name, location, conf = mon["monument"], mon["location"], mon["confidence"]
        prompt = (
            f"The monument '{name}' located at '{location}' was identified with {conf}% confidence.\n"
            f"Include:\n1. Exact Location: {location}\n2. Architectural & Historical Highlights\n"
            f"3. Spiritual/Cultural Significance\n4. Best Time to Visit & Visitor Tips.\n"
            f"Reply ONLY in {lname}."
        )
        details = run_llm(prompt, f"Tell me about {name} located at {location}.")
        answer = f"🏛 Monument Identified: **{name}** ({conf}% Confidence)\n📍 Location: **{location}**\n\n{details}"
        return {"status": "ok", "intent": "monument", "answer": answer, "lang": lang}

    # 3. If image was detected as a person / yoga pose instead of a monument
    detected_type = mon.get("detected_type", "")
    if "yoga" in detected_type or "person" in detected_type:
        prompt = (
            f"The user uploaded an image showing a person or exercise/yoga posture.\n"
            f"Analyze the posture or provide wellness guidance:\n"
            f"1. Identified Asana or Posture Name\n2. Alignment & Body Posture Guidance\n3. Benefits & Precautions.\n"
            f"Reply ONLY in {lname}."
        )
        analysis = run_vision_llm(prompt, image_path)
        if analysis:
            answer = f"🧘 **Yoga / Posture Evaluation**:\n\n{analysis}"
            return {"status": "ok", "intent": "yoga", "answer": answer, "lang": lang}

    # 4. If clearly not a monument (and no vision analyzer match), state cleanly that it is not a monument
    answer = NOT_A_MONUMENT_MSG.get(lang, NOT_A_MONUMENT_MSG["en"])
    return {"status": "ok", "intent": "general", "answer": answer, "lang": lang}


# ---------------------------------------------------------
# Keywords for Restroom, Weather & Hotels
# ---------------------------------------------------------
TOILET_WORDS = ["toilet", "washroom", "bathroom", "restroom", "शौचालय", "स्वच्छतागृह", "টয়লেট"]
WEATHER_WORDS = ["weather", "temperature", "forecast", "climate", "rain", "मौसम", "तापमान", "हवामान", "আবহাওয়া"]
HOTEL_WORDS = [
    "hotel", "hotels", "homestay", "homestays", "resort", "resorts", "lodge", "lodges",
    "lodging", "stay", "stays", "accommodation", "dharamshala", "ashram",
    "होटल", "धर्मशाला", "होमस्टे", "हॉटेल", "হোটেল", "রিসোর্ট"
]

TOILET_KNOWN = [
    (["sudhowala", "सुधोवाला"], "🚻 Public restrooms near Sudhowala:\n1. Sudhowala Bus Stop / Main Road Complex\n2. Near Prem Nagar Market & Uttaranchal University vicinity\n3. ISBT Dehradun Public Toilet Complex."),
    (["dehradun", "देहरादून", "clock tower"], "🚻 Public restrooms in Dehradun:\n1. Clock Tower Public Toilet Complex (Paltan Bazaar entrance)\n2. Dehradun Railway Station & Parade Ground\n3. ISBT Dehradun Main Terminal."),
    (["kedarnath", "केदारनाथ"], "🚻 Public restrooms in Kedarnath:\n1. Gaurikund Base Camp & Trekking Route Points\n2. Lincholi & Bheembali Halt Points\n3. Kedarnath Temple Outer Complex."),
    (["rishikesh", "ऋषिकेश"], "🚻 Public restrooms in Rishikesh:\n1. Main Bus Stand & GMVN Rest House\n2. Near Laxman Jhula & Ram Jhula entrances\n3. Triveni Ghat Promenade."),
]


def _handle_toilet(q, user_input, lang):
    for keys, reply in TOILET_KNOWN:
        if contains_any(q, keys):
            return {"status": "ok", "intent": "toilet", "answer": reply, "lang": lang}
    loc = extract_city(user_input)
    prompt = (
        f"Provide public restroom guidance for tourists in '{loc}'. Suggest up to 3 typical public "
        f"locations (bus stand, railway station, market). Say these are general suggestions and "
        f"should be confirmed locally. Reply ONLY in {lang_name(lang)}."
    )
    return {"status": "ok", "intent": "toilet", "answer": run_llm(prompt, user_input), "lang": lang}


def _handle_weather(user_input, lang):
    place = extract_city(user_input)
    res = get_live_weather(place, lang=lang)
    msg = res.get("formatted", f"Weather information for {place}.")
    crowd = predict_crowd(place)
    if crowd:
        msg += f"\n• **Estimated Visitor Footfall**: {crowd}"
    return {"status": "ok", "intent": "weather", "answer": msg, "lang": lang}


def _handle_hotel(user_input, lang):
    place = extract_city(user_input)
    hotel_info = get_hotel_recommendations(place, lang=lang)
    return {"status": "ok", "intent": "hotel", "answer": hotel_info, "lang": lang}


# ---------------------------------------------------------
# TTS Audio Attachment
# ---------------------------------------------------------
def _attach_tts(result, lang):
    answer = result.get("answer")
    if (
        generate_tts_audio
        and isinstance(answer, str)
        and not is_llm_error(answer)
        and not result.get("audio_url")
    ):
        audio = generate_tts_audio(answer, lang=LANG_MAP[lang]["tts"])
        if audio:
            result["audio_url"] = audio
    return result


# =========================================================
# MAIN ROUTER
# =========================================================
def ai_router(
    user_input: str,
    lang: str = "en",
    persona: str = "travel_guide",
    image_path: Optional[str] = None,
):
    lang = lang if lang in LANG_MAP else "en"
    lname = lang_name(lang)
    intent = classify_intent(user_input)
    q = (user_input or "").lower()
    persona_prompt = get_persona(persona)

    # 1. Image handling (Monuments / Yoga)
    if image_path and os.path.isfile(image_path):
        return _attach_tts(_handle_image(intent, lang, image_path), lang)

    # 2. Public Restrooms
    if contains_any(q, TOILET_WORDS):
        result = _handle_toilet(q, user_input, lang)

    # 3. Live Weather & Climate Guide (OpenWeather + Gemini fallback)
    elif contains_any(q, WEATHER_WORDS):
        result = _handle_weather(user_input, lang)

    # 4. Hotels, Homestays & Ashrams (Curated Catalog + Gemini fallback)
    elif contains_any(q, HOTEL_WORDS):
        result = _handle_hotel(user_input, lang)

    # 5. Meditation flow
    elif is_meditation_reply(q, intent):
        med = handle_meditation(lang, user_input)
        result = {
            "status": "ok",
            "intent": "meditation",
            "answer": med["answer"],
            "audio_url": med["audio_url"],
            "lang": lang,
        }

    # 6. Yoga Instruction
    elif intent == "yoga":
        prompt = (
            f"{persona_prompt}\nYou are an expert Yoga instructor. Recommend yoga postures (Asanas) with "
            f"step-by-step instructions, breathing guidance (Pranayama), benefits and precautions. "
            f"Reply ONLY in {lname}."
        )
        result = {"status": "ok", "intent": "yoga", "answer": run_llm(prompt, user_input), "lang": lang}

    # 7. Monument History & Architecture
    elif intent == "monument":
        prompt = (
            f"{persona_prompt}\nProvide historical, architectural and pilgrimage information about "
            f"monuments and temples. Reply ONLY in {lname}."
        )
        result = {"status": "ok", "intent": "monument", "answer": run_llm(prompt, user_input), "lang": lang}

    # 8. Spiritual Knowledge (Gita, Shlokas, Temples with Gemini fallback)
    elif intent == "spiritual":
        ans = answer_spiritual_rag(user_input, lang=lang)
        result = {"status": "ok", "intent": "spiritual", "answer": _with_intro(ans, lang), "lang": lang}

    # 9. Tourism & Travel Guide (Dataset RAG with Gemini fallback)
    elif intent == "tourism":
        ans = answer_tourism_rag(user_input, lang=lang)
        result = {"status": "ok", "intent": "tourism", "answer": _with_intro(ans, lang), "lang": lang}

    # 10. General Tourism / Multi-topic Assistance
    else:
        system = (
            f"{persona_prompt}\nSTRICT RULES:\n- Answer ONLY in {lname}\n"
            f"- Use clear headings, separate lines, and bullet points for readability."
        )
        result = {
            "status": "ok",
            "intent": "general",
            "answer": _with_intro(run_llm(system, user_input), lang),
            "lang": lang,
        }

    return _attach_tts(result, lang)