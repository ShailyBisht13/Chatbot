# realtime_services.py
import requests

# ---------------------------
# LIVE WEATHER API
# ---------------------------
def get_live_weather(location: str):
    """
    Returns current weather for a location using OpenWeather API.
    """
    try:
        API_KEY = "YOUR_OPENWEATHER_KEY_HERE"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") != 200:
            return f"Weather not found for {location}"

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].title()

        return f"Weather in {location}: {temp}°C, {desc}"

    except Exception as e:
        return f"Weather service error: {str(e)}"


# ---------------------------
# CROWD PREDICTION
# ---------------------------
def get_live_crowd(place: str):
    """
    Simple mock crowd prediction (upgrade later with real models).
    """
    place = place.lower()

    if "kedarnath" in place:
        return "Crowd Level: HIGH (Peak Yatra season from May–June)"
    if "badrinath" in place:
        return "Crowd Level: MODERATE during weekends"
    if "hemkund" in place:
        return "Crowd Level: LOW except pilgrimage months"

    return "Current crowd load: Moderate"


# ---------------------------
# HOTEL / HOMESTAY API
# ---------------------------
def get_hotel_recommendations(location: str):
    """
    Returns affordable homestay recommendations.
    Replace the mock API with real tourism API.
    """
    dummy_data = {
        "rishikesh": [
            {"name": "Ganga Riverside Homestay", "price": "₹800/night"},
            {"name": "Yoga Retreat Stay", "price": "₹1200/night"}
        ],
        "kedarnath": [
            {"name": "GMVN Kedarnath Cottages", "price": "₹1500/night"},
            {"name": "Bhakt Niwas", "price": "₹600/night"}
        ]
    }

    location = location.lower()
    if location in dummy_data:
        return dummy_data[location]

    return [{"name": "No hotels found", "price": "-"}]
