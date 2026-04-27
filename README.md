<p align="center">
  <h1 align="center">🌾 AgroCast AI</h1>
  <p align="center"><strong>Smart Mandi Price & Logistics Advisory for Indian Farmers</strong></p>
  <p align="center">
    <em>Built at <strong>Aurelion Hackathon</strong> — Karunya University | 27 Feb 2026</em>
  </p>
  <p align="center">
    <a href="#features">Features</a> •
    <a href="#tech-stack">Tech Stack</a> •
    <a href="#team--contributions">Team</a> •
    <a href="#setup">Setup</a> •
    <a href="#architecture">Architecture</a>
  </p>
</p>

---

## Overview

AgroCast is an AI-driven agricultural market intelligence platform that empowers Indian farmers with **real-time, actionable insights** via voice interaction in regional languages. Speak a query in Tamil, Hindi, Malayalam, or Telugu — and instantly get live mandi prices, transportation logistics, weather data, and a bilingual AI advisory recommending the most profitable market to sell your crop.

> *"Coimbatore mein tamatar ka kya price chal raha hai?"* → Instant market comparison with transport cost analysis.

---

## Features

- 🎙️ **Voice-First Interface** — Speak naturally in 4 Indian languages (Tamil, Hindi, Malayalam, Telugu)
- 📊 **Live Mandi Prices** — Real-time data from Government of India (data.gov.in / Agmarknet)
- 🗺️ **Smart Logistics** — OSRM-powered driving distance + transport cost calculation
- 🤖 **AI Advisory** — Bilingual recommendations via DeepSeek V3 (Featherless AI)
- 🔊 **Text-to-Speech** — Regional language audio output via ElevenLabs + gTTS
- 🌤️ **Live Weather & AQI** — Real-time environmental data via Open-Meteo
- 📞 **Twilio IVR** — Phone-based voice access for farmers without smartphones
- 📈 **Premium Dashboard** — Glassmorphism UI with market comparison cards

---

## Team & Contributions

> 🏆 **Aurelion Hackathon** — Karunya University, 27 February 2026

### 👤 Azriel Gershom Raj — *Full-Stack AI Pipeline Architect*
> **Core Backend + AI Engine + Frontend Dashboard**

| Area | Work Done |
|------|-----------|
| **FastAPI Backend** | Designed and built the entire `/predict` pipeline (`api/main.py`) — the central orchestrator that connects voice input → data extraction → market analysis → AI advisory → audio synthesis |
| **Market Intelligence Engine** | Built the complete market data module (`services/market_data.py`) — live Government API integration, dual-pass geospatial sorting (Haversine + OSRM), transport cost estimation, net-profit comparison logic, and dynamic fallback data synthesizer |
| **Bilingual AI Advisory** | Engineered the multi-intent LLM prompt system (price_check / climate_check / full_advice) that generates structured bilingual advisories in regional script + English using DeepSeek V3 |
| **Streamlit Dashboard** | Built the complete premium frontend (`frontend/app.py`) — 800+ lines of glassmorphism UI with voice recording, market comparison cards, price bars, weather strip, translated data tables, and auto-playing TTS audio |
| **Integration & Architecture** | Wired together all services end-to-end: voice → NLP entity extraction → market API → geospatial routing → LLM generation → speech synthesis → UI rendering |

---

### 👤 Jonathan Joseph — *Geospatial & Voice IVR Engineer*

| Area | Work Done |
|------|-----------|
| **Twilio IVR Microservice** | Built the complete phone-based voice access system (`services/twilio_service.py`) — IVR call flow with language selection, speech-to-text capture, AI processing, and gTTS audio response back to the caller |
| **Geocoding System** | Implemented the geocoding pipeline with persistent JSON caching (`GeocodingCache`), Nominatim API integration, and 40+ pre-cached Indian city coordinates for instant lookups |
| **OSRM Routing Integration** | Integrated the Open Source Routing Machine API for real driving distance and duration calculations between farmer location and distant markets |
| **Data Pipeline Setup** | Configured the Government of India data.gov.in API connection with multi-state market search and robust error handling |

---

### 👤 Preetham — *ML & Environmental Intelligence*

| Area | Work Done |
|------|-----------|
| **ML Model Pipeline** | Built the environmental AQI forecasting model using scikit-learn (`ml/create_mock_models.py`) — Linear Regression trained on temperature, humidity, and precipitation features |
| **Weather & AQI Services** | Developed the live data fetcher module (`services/fetcher.py`) — Open-Meteo API integration for real-time temperature, humidity, precipitation, and European AQI |
| **Speech Recognition** | Implemented the voice input processing pipeline — audio recording, WAV file handling, Google Speech Recognition API integration, and multi-language transcription |
| **Testing Suite** | Created API endpoint tests (`tests/test_api.py`) and TTS integration tests (`tests/test_tts.py`) to validate the prediction pipeline and ElevenLabs audio generation |

---

### 👤 Manas Deep — *UI Design & DevOps*

| Area | Work Done |
|------|-----------|
| **UI/UX Design System** | Designed the complete CSS theme — dark agri-tech color palette, glassmorphism cards, gradient price bars, metric pills, best-market badges, pulse animations, and responsive layouts |
| **Localization Layer** | Built the multi-language UI translation system (`UI_TRANSLATIONS`) — native script button labels, localized table headers, and dynamic language switching across Tamil, Hindi, Malayalam, and Telugu |
| **Deployment Configuration** | Set up Docker containerization (`Dockerfile`), Heroku/Render deployment (`Procfile`), Streamlit cloud config (`scripts/setup.sh`), and the multi-service launcher (`scripts/run_all.ps1`) |
| **Documentation** | Authored the project technical report (`docs/project_report.md`) covering architecture, module descriptions, and the full technology stack |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit, Custom CSS/HTML, Pandas |
| **Backend API** | FastAPI, Uvicorn, Pydantic |
| **AI/LLM** | Featherless AI (DeepSeek V3), OpenAI SDK |
| **Speech** | SpeechRecognition, ElevenLabs, gTTS |
| **Geospatial** | Geopy (Nominatim), OSRM Routing |
| **Data Sources** | data.gov.in API, Open-Meteo API |
| **ML** | scikit-learn, joblib |
| **Voice IVR** | Twilio, FastAPI |

---

## Project Structure

```
AgroCast-Backend/
├── api/                        # FastAPI backend
│   ├── __init__.py
│   └── main.py                 # Core API — /predict endpoint
│
├── services/                   # Business logic modules
│   ├── __init__.py
│   ├── fetcher.py              # Weather & AQI data fetchers
│   ├── market_data.py          # Mandi price engine & logistics
│   └── twilio_service.py       # Twilio IVR microservice
│
├── ml/                         # Machine learning models
│   ├── __init__.py
│   └── create_mock_models.py   # Script to generate mock .pkl models
│
├── frontend/                   # Streamlit dashboard
│   └── app.py                  # Voice-interactive market advisory UI
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_api.py             # API endpoint tests
│   └── test_tts.py             # TTS integration tests
│
├── scripts/                    # Runner & deployment scripts
│   ├── run_all.ps1             # Windows — launch all services
│   ├── run_demo.py             # Twilio IVR demo launcher
│   └── setup.sh                # Streamlit cloud config
│
├── docs/                       # Documentation
│   └── project_report.md       # Full technical report
│
├── static/                     # Generated audio files (gitignored)
├── .env.example                # Environment variable template
├── .gitignore
├── Dockerfile
├── Procfile
├── requirements.txt
├── requirements_frontend.txt
├── LICENSE
└── README.md
```

---

## Setup

### Prerequisites
- Python 3.10+
- pip

### 1. Clone & Install

```bash
git clone https://github.com/Jonathan-Joseph-2007/AgroCast-Backend.git
cd AgroCast-Backend

python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\Activate.ps1     # Windows

pip install -r requirements.txt
pip install -r requirements_frontend.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your API keys:
#   FEATHERLESS_API_KEY=...
#   ELEVENLABS_API_KEY=...
```

### 3. Generate ML Models (first time only)

```bash
python -m ml.create_mock_models
```

### 4. Run the Application

**Terminal 1 — FastAPI Backend:**
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 — Streamlit Frontend:**
```bash
streamlit run frontend/app.py
```

**Terminal 3 — Twilio IVR (optional):**
```bash
python scripts/run_demo.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/predict` | Main prediction pipeline |

### Example Request

```json
{
  "crop": "Tomato",
  "yield_amount": 2500,
  "location": "Coimbatore",
  "language": "Tamil",
  "intent": "full_advice"
}
```

---

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌────────────────────┐
│  Voice Input │────▶│  Streamlit   │────▶│   FastAPI Backend   │
│  (Mic/Phone) │     │  Frontend    │     │   /predict          │
└──────────────┘     └──────────────┘     └─────────┬──────────┘
                                                    │
                     ┌──────────────────────────────┼──────────────────┐
                     │                              │                  │
              ┌──────▼──────┐  ┌───────────▼────────┐  ┌──────▼──────┐
              │ data.gov.in │  │ Featherless AI     │  │ Open-Meteo  │
              │ Mandi API   │  │ (DeepSeek V3)      │  │ Weather/AQI │
              └─────────────┘  └────────────────────┘  └─────────────┘
```

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <sub>Built with ❤️ for Indian Farmers at <strong>Aurelion Hackathon 2026</strong> — Karunya University</sub>
</p>
