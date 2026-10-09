# 🕉️ SHIVA BOT — AI Tourism, Spiritual & Wellness Assistant

SHIVA BOT is an intelligent, multimodal AI assistant designed for Indian Tourism, Spiritual Heritage, Yoga Posture Analysis, Real-time Weather, Hotel/Homestay Guidance, and Ambient Meditation.

---

## 🚀 Key Features

1. **🧭 Intelligent Tourism Guide (Local RAG + Google Gemini Fallback)**
   - RAG-powered vector search across Indian destinations (`tourism_embeds.pt`).
   - Automatically utilizes **Google Gemini** for unseen destinations, generating comprehensive itineraries (1/3/5 days), transport options (air/rail/road), best seasons, and local food.

2. **🕉️ Spiritual & Heritage Intelligence**
   - In-depth coverage of the Bhagavad Gita, Sanskrit Shlokas, Puranic mythology, Char Dham, and temple heritage.
   - Word-by-word Sanskrit translations and modern spiritual context.

3. **🌦️ Live Weather & Climate Advisory (OpenWeather API + Gemini)**
   - Real-time weather data (temperature, feels-like, humidity, wind speed) via OpenWeather API.
   - Intelligent seasonal climate advisories, crowd level forecasts, and packing checklists.

4. **🏨 Curated Homestays & Hotel Recommendations**
   - Curated directory for top pilgrimage & travel hubs (Rishikesh, Kedarnath, Badrinath, Varanasi, Jaipur, Goa, Munnar).
   - Dynamic Gemini fallback for remote destinations, recommending GMVN/KMVN guest houses, verified homestays, and ashrams with approximate INR pricing.

5. **🧘 Yoga Posture & Wellness Engine**
   - MobileNetV2 / TFLite classifier trained across 87 Yoga Asanas (`yoga_mobilenetv2.tflite`).
   - Multimodal posture evaluation via **Gemini Vision** providing alignment corrections, benefits, and breathing (*Pranayama*) tips.

6. **🏛️ Zero-Shot Monument Recognition**
   - CLIP Vision model for recognizing Indian historical monuments & heritage sites.
   - Strict rejection logic prevents non-monuments (e.g. selfies, yoga postures) from false matches.

7. **🎵 Ambient Meditation Generator**
   - Generates loopable ambient meditation tracks (Forest, River, Mountain Wind, Rain) with guided mindfulness prompts.

8. **🗣️ Multilingual Speech & Regional Support**
   - Supports English, Hindi, Bengali, Marathi, and Sanskrit.
   - Includes 10,000+ regional dialect entries for Garhwali and Kumaoni (`datasets/regional/`).
   - Server-side Text-to-Speech (gTTS) generation.

---

## 🏗️ System Architecture

```
[ Frontend: React.js ] (Port 3000)
         │
         ▼ (REST API)
[ Backend: Node.js / Express ] (Port 5000)
         │
         ▼ (HTTP JSON)
[ AI Engine: FastAPI / Python ] (Port 8000)
    ├── Local Vector Embeddings (PyTorch / SentenceTransformers)
    ├── Dual LLM Provider (Google Gemini + Groq)
    ├── Live OpenWeather API
    ├── CLIP Vision & TFLite Yoga Models
    └── Ambient Meditation Engine
```

---

## 📦 Project Structure

```
projectds/
├── ai_engine/
│   ├── datasets/
│   │   ├── regional/          # Garhwali & Kumaoni datasets
│   │   ├── spiritual/         # Gita CSV, Shlokas & Temples JSON
│   │   ├── tourism/           # Indian travel datasets
│   │   └── yoga/              # Yoga dataset links
│   ├── general/               # Facts, emergency numbers, eco-tips
│   ├── models/                # Verified PyTorch (.pt) & TFLite models
│   ├── prompts/               # System prompt templates
│   ├── sounds/                # Ambient sound audio files (.mp3)
│   ├── ai_server.py           # FastAPI AI Server (Port 8000)
│   ├── router.py              # Central Intent & Routing Engine
│   ├── llm_engine.py          # Unified Gemini & Groq LLM Provider
│   ├── realtime_services.py   # Live Weather & Hotel Services
│   ├── tourism_rag.py         # Tourism RAG with Gemini Fallback
│   ├── spiritual_rag.py       # Spiritual RAG Engine
│   ├── monuments_ai.py        # CLIP Monument Vision Classifier
│   ├── meditation_engine.py   # Meditation Audio Engine
│   └── yoga_server.py         # Yoga Pose Inference Server (Port 5005)
├── backend/
│   ├── config/                # Backend environment configuration
│   ├── middleware/            # JWT authentication middleware
│   ├── models/                # MongoDB User & Chat models
│   ├── routes/                # Auth, Chat, Storage & Upload routes
│   └── index.js               # Express Server Entry Point (Port 5000)
├── frontend/
│   ├── public/                # Static assets & HTML template
│   └── src/                   # React components, pages & services
├── tests/                     # Unit & verification test suite
└── requirements.txt           # Python dependencies
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- **Node.js** (v18+)
- **Python** (v3.9+)
- **MongoDB** (Local or MongoDB Atlas)

---

### 2. Configure Environment Variables
Create or update `config/keys.env` or `.env` in `projectds/`:

```ini
# Groq API Key (Fast completions)
GROQ_API_KEY=your_groq_api_key

# Google Gemini API Key (Multimodal & Fallback Intelligence)
GEMINI_API_KEY=your_gemini_api_key

# OpenWeather API Key (Real-time Weather)
OPENWEATHER_API_KEY=your_openweather_api_key

# Backend Configuration
PORT=5000
JWT_SECRET=your_jwt_secret_key
MONGO_URI=mongodb://127.0.0.1:27017/projectds
```

---

### 3. Install Dependencies

#### Python AI Engine:
```bash
pip install -r requirements.txt
```

#### Node.js Backend:
```bash
cd backend
npm install
```

#### React Frontend:
```bash
cd frontend
npm install
```

---

## 🚀 Running the Application

Open **3 separate terminal windows**:

### Terminal 1: 🤖 AI Engine
```bash
cd ai_engine
python -m uvicorn ai_server:app --host 127.0.0.1 --port 8000 --reload
```
*(Runs on: `http://127.0.0.1:8000`)*

### Terminal 2: ⚙️ Backend Server
```bash
cd backend
npm start
```
*(Runs on: `http://localhost:5000`)*

### Terminal 3: 💻 Frontend UI
```bash
cd frontend
npm start
```
*(Runs on: `http://localhost:3000`)*

---

## 🧪 Testing & Verification

Run the test suite from `projectds/`:
```bash
python tests/check_models.py
python tests/verify_meditation.py
```

---

## 📜 License
This project is licensed under the ISC License.
