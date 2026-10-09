# realtime_services.py — Live Weather (OpenWeather API + Gemini fallback), Hotels/Homestays & Crowd Predictions
import os
import requests
import logging
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load env variables
for env_path in [
    os.path.join(BASE_DIR, "..", "config", "keys.env"),
    os.path.join(BASE_DIR, "..", ".env"),
    os.path.join(BASE_DIR, "config", "keys.env"),
    os.path.join(BASE_DIR, ".env"),
    "config/keys.env",
    ".env",
]:
    if os.path.exists(env_path):
        load_dotenv(env_path)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# ---------------------------------------------------------
# 1. LIVE WEATHER API (OpenWeather + Gemini/LLM Fallback)
# ---------------------------------------------------------
def get_live_weather(location: str, lang: str = "en") -> Dict[str, Any]:
    """
    Fetches real-time weather using OpenWeather API.
    If OpenWeather key is absent or location is not found in OpenWeather,
    it automatically falls back to Gemini/LLM for seasonal weather & climate advice.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY") or OPENWEATHER_API_KEY

    # 1. Try OpenWeather API if key is present
    if api_key and api_key != "YOUR_OPENWEATHER_KEY_HERE":
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": location,
                "appid": api_key,
                "units": "metric",
                "lang": lang if lang in ["hi", "bn", "mr", "en"] else "en",
            }
            res = requests.get(url, params=params, timeout=6)
            if res.status_code == 200:
                data = res.json()
                city = data.get("name", location)
                country = data.get("sys", {}).get("country", "IN")
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                condition = data["weather"][0]["description"].title()
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]

                formatted = (
                    f"🌦 **Current Live Weather in {city}, {country}**:\n"
                    f"• **Temperature**: {temp}°C (Feels like {feels_like}°C)\n"
                    f"• **Condition**: {condition}\n"
                    f"• **Humidity**: {humidity}%\n"
                    f"• **Wind Speed**: {wind_speed} m/s"
                )

                return {
                    "status": "ok",
                    "source": "openweather",
                    "location": f"{city}, {country}",
                    "temperature": f"{temp}°C",
                    "condition": condition,
                    "humidity": f"{humidity}%",
                    "wind_speed": f"{wind_speed} m/s",
                    "formatted": formatted,
                }
        except Exception as e:
            logger.warning("OpenWeather request failed for %s: %s", location, e)

    # 2. Fallback to Gemini / LLM when OpenWeather is not available or location is missing
    from llm_engine import run_llm
    from languages import lang_name

    prompt = (
        f"You are a weather and climate advisor for travelers in India.\n"
        f"Provide a realistic seasonal weather, temperature range, and travel clothing advisory for '{location}'.\n"
        f"Include typical morning/evening temperatures, rainfall chances, and packing tips.\n"
        f"Reply ONLY in {lang_name(lang)} with neat bullet points."
    )
    fallback_report = run_llm(prompt, f"What is the weather and climate guide for visiting {location}?")

    return {
        "status": "ok",
        "source": "gemini_climate_guide",
        "location": location,
        "formatted": f"🌦 **Weather & Climate Advisory for {location}**:\n\n{fallback_report}",
    }


# ---------------------------------------------------------
# 2. HOTEL & HOMESTAY DIRECTORY + GEMINI API
# ---------------------------------------------------------
CURATED_HOTELS = {
    "rishikesh": [
        {"name": "Ganga Kinare — A Riverside Boutique Hotel", "type": "Heritage/Luxury", "price": "₹4,500/night", "area": "Veerbhadra Road"},
        {"name": "Zostel Rishikesh (Tapovan)", "type": "Backpacker / Hostel", "price": "₹750 - ₹2,000/night", "area": "Tapovan"},
        {"name": "Anand Kashi by the Ganges", "type": "Eco Retreat", "price": "₹8,000/night", "area": "Badrinath Road"},
        {"name": "Parmarth Niketan Ashram Stays", "type": "Ashram / Spiritual Stay", "price": "₹500 - ₹1,200/night", "area": "Swarg Ashram"},
    ],
    "kedarnath": [
        {"name": "GMVN Kedarnath Swargarohini Complex", "type": "Govt Cottage / Dorm", "price": "₹1,000 - ₹2,500/night", "area": "Near Kedarnath Temple"},
        {"name": "GMVN Base Camp Tents (Lincholi/Gaurikund)", "type": "Alpine Tents", "price": "₹500 - ₹1,200/night", "area": "Gaurikund / Basecamp"},
        {"name": "Shiva Rest House & Bhakt Niwas", "type": "Pilgrim Lodge", "price": "₹600 - ₹1,500/night", "area": "Temple Path"},
    ],
    "badrinath": [
        {"name": "GMVN Hotel Devlok Badrinath", "type": "Govt Tourist Lodge", "price": "₹1,800 - ₹3,500/night", "area": "Near Temple Road"},
        {"name": "Sarovar Portico Badrinath", "type": "Premium Hotel", "price": "₹6,500/night", "area": "Near Bus Stand"},
        {"name": "Manav Kalyan Ashram & Dharamshala", "type": "Budget Ashram", "price": "₹400 - ₹1,000/night", "area": "Bamni Village Road"},
    ],
    "varanasi": [
        {"name": "BrijRama Palace Varanasi", "type": "Heritage Palace", "price": "₹12,000/night", "area": "Darbhanga Ghat"},
        {"name": "Scindhia Guest House", "type": "Riverside Homestay", "price": "₹1,500 - ₹3,000/night", "area": "Scindia Ghat"},
        {"name": "Zostel Varanasi", "type": "Hostel & Private Rooms", "price": "₹600 - ₹1,800/night", "area": "Dashashwamedh Road"},
    ],
    "jaipur": [
        {"name": "Shahpura Haveli Jaipur", "type": "Heritage Homestay", "price": "₹3,500/night", "area": "Bani Park"},
        {"name": "RTDC Hotel Gangaur", "type": "State Tourism Hotel", "price": "₹1,600/night", "area": "MI Road"},
        {"name": "Umaid Bhawan Heritage House", "type": "Boutique Hotel", "price": "₹2,800/night", "area": "Collectorate Circle"},
    ],
    "goa": [
        {"name": "Casa da Praia Homestay", "type": "Portuguese Villa Homestay", "price": "₹2,500/night", "area": "Candolim, North Goa"},
        {"name": "Fontainhas Heritage House", "type": "Heritage Stay", "price": "₹2,200/night", "area": "Latin Quarter, Panaji"},
        {"name": "Palolem Beach Eco Huts", "type": "Beach Cottages", "price": "₹1,200 - ₹2,800/night", "area": "Palolem, South Goa"},
    ],
    "munnar": [
        {"name": "KTDC Tea County", "type": "State Resort", "price": "₹3,800/night", "area": "KTDC Hill"},
        {"name": "Munnar Valley Homestay & Spice Garden", "type": "Eco Homestay", "price": "₹1,400/night", "area": "Old Munnar"},
    ],
}


def get_hotel_recommendations(location: str, lang: str = "en") -> str:
    """
    Returns hotel, homestay, and ashram options for the specified location.
    1. Checks local curated catalog first.
    2. If not present in catalog, queries Gemini/LLM to generate authentic recommendations.
    """
    loc_clean = (location or "").lower().strip()

    # 1. Match local curated catalog
    matched_key = None
    for key in CURATED_HOTELS:
        if key in loc_clean or loc_clean in key:
            matched_key = key
            break

    if matched_key:
        stays = CURATED_HOTELS[matched_key]
        lines = [f"🏨 **Top Verified Homestays & Accommodations in {matched_key.title()}**:\n"]
        for s in stays:
            lines.append(f"• **{s['name']}** ({s['type']})\n  📍 *Location*: {s['area']} | 💵 *Price*: {s['price']}")
        lines.append("\n💡 *Tip: Advance booking is highly recommended during peak tourist and festival seasons.*")
        return "\n".join(lines)

    # 2. When not present in local catalog, query Gemini/LLM for rich recommendations
    from llm_engine import run_llm
    from languages import lang_name

    system = (
        f"You are a hospitality and accommodation guide for travelers across India.\n"
        f"Recommend 3 to 4 reputable accommodations (including government tourist lodges like GMVN/KMVN/RTDC/KTDC, verified homestays, ashrams, and boutique hotels) for '{location}'.\n"
        f"For each stay, include:\n"
        f"1. Name & Type (Homestay, Govt Lodge, Heritage Stay, Ashram)\n"
        f"2. Approximate Price Range per night in INR\n"
        f"3. Key Amenities & Nearby Landmark\n"
        f"4. Booking Tip (Govt portal, walk-in, online)\n\n"
        f"Reply ONLY in {lang_name(lang)} with clear headings and bullet points."
    )
    return run_llm(system, f"Recommend best homestays and hotels in {location}.")


# ---------------------------------------------------------
# 3. CROWD PREDICTION
# ---------------------------------------------------------
def get_live_crowd(place: str) -> str:
    p = place.lower()
    if "kedarnath" in p or "badrinath" in p or "gangotri" in p or "yamunotri" in p:
        return "Peak Yatra Season (High traffic May-June & Sept-Oct). Registration required."
    if "varanasi" in p or "kashi" in p:
        return "Heavy evening footfall near Dashashwamedh & Kashi Vishwanath corridors."
    if "goa" in p:
        return "High tourist traffic November to February; moderate in monsoon."
    if "jaipur" in p or "rajasthan" in p:
        return "Peak winter season footfall from October to March."
    return "Normal to Moderate visitor volume."
