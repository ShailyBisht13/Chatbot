# 🕉️ DeepShiva

**An AI-powered assistant for spiritual tourism, guidance, and cultural exploration in the Himalayan region.**

DeepShiva (the bot introduces itself as *SHIVA BOT*) helps pilgrims and travellers plan visits to temples and sacred places in Uttarakhand and beyond. It answers questions about spirituality, travel, weather, and culture, guides meditation and yoga, and can identify monuments from photos, by text, by voice, or with audio.

---

## ✨ Features

| Feature | What it does |
|---|---|
| **Spiritual guidance & temple information** | Answers questions about temples, deities, legends, and pilgrimage practices using a spiritual knowledge base (RAG). |
| **Tourism assistance for Himalayan regions** | Routes, stays, permits, what to carry, and trip planning, grounded in a tourism knowledge base. |
| **Nearby temples & sacred places** | Suggests sacred sites and points of interest around a location. |
| **Guided meditation & mindfulness** | A 1-minute guided meditation with a chosen ambient sound (forest, river, wind, rain). |
| **Festivals, rituals & cultural knowledge** | Explains festivals, rituals, customs, and traditions. |
| **Audio guidance & chants** | Replies are converted to speech (text-to-speech) so answers can be listened to. |
| **Voice-based interaction** | Ask questions by speaking instead of typing. |
| **Multilingual support** | English and Hindi in the UI. The backend router also handles Sanskrit, Marathi, and Bengali replies. |
| **Travel tips & local insights** | Practical advice such as restrooms, safety, and local etiquette. |
| **Best time to visit spiritual places** | Seasonal guidance, combined with live weather and crowd estimates. |

**Extras built into the backend**

- 🌦 **Live weather** for a city or town, with an estimated visitor-crowd level.
- 🧘 **Yoga help**: asana instructions, pranayama, benefits, and precautions. Upload a pose photo for feedback.
- 🏛 **Monument recognition**: upload a photo and the bot identifies the monument, its location, and its history.
- 🗣 **Kumaoni / Garhwali dataset lookup** (`data_engineer.py`) for regional-language answers.

---

## 🧱 Architecture

```
React frontend (localhost:3000)
        │
        ▼
FastAPI  (api.py)  ──►  ai_router(...)   ← main brain (router.py)
                            │
        ┌───────────┬───────┼──────────┬────────────┐
        ▼           ▼       ▼          ▼            ▼
   Intent      Tourism /  Weather +  Meditation   Monument /
   classifier  Spiritual  crowd      + Yoga       Yoga image
               RAG        prediction (LLM + audio) analysis
                            │
                            ▼
                    LLM engine (Groq)  ──►  Text-to-speech
```

**How a request flows**

1. The user sends a message (text, voice, or image) with a language.
2. The router classifies the **intent** (spiritual, tourism, meditation, yoga, monument, weather, general).
3. It calls the matching module: RAG, weather API, meditation audio, image recognition, or the LLM.
4. The answer is returned as text, plus an `audio_url` when speech is generated.

---

## 📁 Project structure

| File | Purpose |
|---|---|
| `router.py` | Main multi-function router that decides how each query is handled. |
| `ai_router.py` | Thin alias that exposes `ai_router()` with a `persona_name` option. |
| `api.py` | FastAPI server exposing the `/chat` endpoint. |
| `llm_engine.py` | Groq LLM client with model fallback. |
| `data_engineer.py` | Kumaoni / Garhwali CSV lookup engine. |
| `realtime_services.py` | Weather, crowd, and hotel helper functions (prototype). |
| `tourism_ai.py` | Simple tourism-prompt LLM helper. |
| `intent_classifier.py`, `tourism_rag.py`, `spiritual_rag.py`, `monuments_ai.py`, `persona_manager.py`, `crowd_prediction.py`, `voice_output.py`, `meditation_engine.py` | Supporting modules used by the router. |

---

## 🚀 Getting started

### Prerequisites
- Python 3.10+
- Node.js (for the React frontend)
- A [Groq](https://groq.com) API key
- An [OpenWeather](https://openweathermap.org/api) API key

### Backend

```bash
pip install fastapi uvicorn requests python-dotenv groq
```

Create `config/keys.env`:

```env
GROQ_API_KEY=your_groq_key_here
OPENWEATHER_API_KEY=your_openweather_key_here
```

> ⚠️ **Never commit API keys.** Add `config/keys.env` and `.env` to `.gitignore`.

Run the server:

```bash
uvicorn api:app --reload --port 8000
```

### Frontend

```bash
npm install
npm start      # opens http://localhost:3000
```

---

## 🔌 API

### `POST /chat`

**Request**
```json
{
  "message": "What is the best time to visit Kedarnath?",
  "language": "en",
  "user_id": "optional-user-id"
}
```

**Response**
```json
{
  "status": "ok",
  "intent": "tourism",
  "answer": "I am SHIVA BOT — your Tourism & Spiritual assistant. ...",
  "audio_url": "/audio/reply_123.mp3",
  "lang": "en"
}
```

Supported language codes: `en`, `hi`, `sa`, `mr`, `bn`.

---

## 💬 Suggested questions to try

### 🛕 Spiritual guidance & temples
- Who is Lord Shiva and why is Kedarnath important?
- What is the story behind the Kedarnath temple?
- What is the significance of Har Ki Pauri and the Ganga Aarti?
- What are the Char Dham and Panch Kedar?
- What should I know before entering a temple? (dress code, etiquette)

### 🏔 Tourism in the Himalayas
- Plan a 3-day trip to Rishikesh and Haridwar.
- How do I reach Kedarnath from Dehradun?
- What should I pack for the Char Dham Yatra?
- Is registration required for the Kedarnath Yatra?
- Which places can I visit around Badrinath?

### 📍 Nearby temples & sacred places
- Which temples are near Rishikesh?
- Suggest sacred places near Haridwar.
- What are the famous temples of Uttarakhand?

### 🧘 Meditation & yoga
- Start a guided meditation.
- I'd like a meditation with river sounds.
- Suggest yoga poses to reduce stress.
- What are the benefits of Surya Namaskar?
- Teach me Anulom Vilom pranayama.

### 🎉 Festivals & culture
- What is the Kumbh Mela and when is it held?
- Tell me about Nanda Devi Raj Jat.
- What is celebrated on Maha Shivratri?
- What are the traditions of Kumaoni and Garhwali culture?

### 🎧 Audio, voice & languages
- Chant the Mahamrityunjaya Mantra. *(audio)*
- मुझे केदारनाथ के बारे में बताइए। *(Hindi)*
- ऋषिकेश में घूमने की जगहें बताइए। *(Hindi)*
- 🎤 Tap the mic and ask: "Which temple should I visit first?"

### 🌦 Weather & best time to visit
- What is the weather in Rishikesh today?
- Current weather in Kedarnath.
- What is the best time to visit Badrinath?
- Is it crowded at Kedarnath right now?

### 🧳 Travel tips & local insights
- Where can I find public toilets near Laxman Jhula?
- What local food should I try in Uttarakhand?
- Is it safe to travel in the monsoon?
- Any tips for first-time high-altitude travellers?

### 📷 Image-based
- *(Upload a temple photo)* Which monument is this and where is it?
- *(Upload a yoga pose photo)* Am I doing this asana correctly?

---

## 🛣 Roadmap

- [ ] Wire the Kumaoni / Garhwali dataset into the router
- [ ] Replace mock hotel and crowd data with live sources
- [ ] Better multilingual weather replies
- [ ] Clean text (no emoji / markdown) before text-to-speech
- [ ] Add tests and error handling around every router branch

---

## 🙏 Acknowledgements

Built with FastAPI, React, Groq LLMs, and OpenWeather. Dedicated to pilgrims and travellers of the Himalayas.

**Har Har Mahadev 🕉️**
