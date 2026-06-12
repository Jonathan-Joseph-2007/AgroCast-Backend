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

# 🏆 Aurelion Hackathon — Karunya University
**Date:** 27 February 2026
**Project:** AI-Powered Multilingual Farmer Market Advisory Platform

---

## 👤 Jonathan Joseph — *Backend Development Engineer*
> Core Area: FastAPI Backend, API Orchestration & Service Integration

| Area | Work Done |
|------|-----------|
| **FastAPI Backend** | Developed the backend application using FastAPI with modular API routing, request handling, and structured response generation. |
| **Prediction Pipeline** | Implemented the `/predict` endpoint to process crop name, farmer location, language preference, and advisory type. |
| **API Orchestration** | Connected multiple backend services including market data, weather data, AI advisory, geospatial routing, and audio response modules. |
| **Request Validation** | Added validation logic for user inputs, missing fields, invalid locations, unsupported languages, and incorrect query formats. |
| **Service Layer Integration** | Integrated service modules using clean backend flow between controller, processing layer, and response layer. |
| **JSON Response Design** | Structured API responses with market comparison data, weather metrics, AQI values, AI advisory text, and audio output path. |
| **Error Handling** | Implemented exception handling for API failures, empty data responses, routing errors, and backend processing issues. |
| **Backend Debugging** | Performed API debugging and endpoint testing to ensure stable communication between frontend and backend modules. |

---

## 👤 Azriel Gershom Raj — *LLM, ML & AI Advisory Architect*
> Core Area: LLM Integration, ML Model Creation & Intelligent Advisory System

| Area | Work Done |
|------|-----------|
| **LLM Integration** | Integrated DeepSeek V3 into the AI advisory workflow for generating intelligent farmer-focused recommendations. |
| **Prompt Engineering** | Designed structured prompts for multiple advisory intents such as price_check, climate_check, and full_advice. |
| **AI Advisory Engine** | Built the advisory logic that combines crop details, market prices, weather conditions, AQI data, and farmer query intent. |
| **ML Model Creation** | Developed the machine learning pipeline for environmental intelligence using scikit-learn-based model creation. |
| **Feature Engineering** | Used weather-related features such as temperature, humidity, precipitation, and AQI values for prediction support. |
| **Bilingual Advisory** | Generated advisory outputs in regional language script along with English translation for better farmer accessibility. |
| **Response Structuring** | Formatted AI responses into clear sections including best market suggestion, price insight, climate alert, and final recommendation. |
| **Output Optimization** | Refined LLM responses to improve relevance, clarity, consistency, and practical usefulness for farmers. |

---

## 👤 Preetham — *Frontend & UI Experience Engineer*
> Core Area: Streamlit Dashboard, UI/UX Design & Farmer Interaction Interface

| Area | Work Done |
|------|-----------|
| **Streamlit Dashboard** | Built the frontend dashboard using Streamlit for crop input, location selection, language selection, and advisory display. |
| **UI Layout** | Designed a clean dashboard layout with input panels, result sections, market comparison cards, and advisory containers. |
| **Market Visualization** | Created frontend components for displaying price comparison, best-market badges, market cards, and profit-related insights. |
| **Weather Display** | Added UI sections for temperature, humidity, rainfall, AQI indicators, and climate-related advisory information. |
| **Voice Interface UI** | Implemented frontend support for voice recording, speech input display, and audio response playback. |
| **Multilingual UI** | Added localized UI text, regional language labels, translated table headers, and dynamic language-based display. |
| **Visual Styling** | Designed glassmorphism cards, dark agri-tech theme, gradient elements, metric pills, animations, and responsive styling. |
| **User Experience** | Improved the dashboard flow to make the system simple, readable, and suitable for farmer-friendly interaction. |

---

## 👤 Manas Deep — *Dataset, Testing & Deployment Engineer*
> Core Area: Dataset Management, Quality Testing & Deployment Configuration

| Area | Work Done |
|------|-----------|
| **Dataset Collection** | Collected and organized crop, market, weather, and environmental data required for project functionality. |
| **Data Preprocessing** | Cleaned, formatted, and structured datasets for backend processing, frontend display, and ML model usage. |
| **Fallback Data System** | Prepared fallback data to maintain system output when live APIs return incomplete or unavailable responses. |
| **API Testing** | Tested backend endpoints with different crops, locations, languages, and advisory types to verify response accuracy. |
| **Integration Testing** | Validated the complete system flow from frontend input to backend processing, AI advisory generation, and final UI rendering. |
| **TTS Testing** | Tested text-to-speech output generation and audio playback integration for voice-based advisory delivery. |
| **Deployment Setup** | Configured Dockerfile, Procfile, setup scripts, environment variables, and project launch commands. |
| **Documentation** | Prepared technical documentation covering dataset usage, testing process, deployment steps, and system workflow. |

---

## Team Contribution Summary

| Team Member | Technical Responsibility |
|-------------|--------------------------|
| Jonathan Joseph | Backend Development, FastAPI, API Orchestration, Service Integration |
| Azriel Gershom Raj | LLM Integration, ML Model Creation, Prompt Engineering, AI Advisory |
| Preetham | Streamlit Frontend, UI/UX Design, Visualization, Multilingual Interface |
| Manas Deep | Dataset Management, Testing, Deployment, Documentation |

---

## Final Project Statement

The team developed an AI-powered multilingual farmer market advisory platform that combines backend APIs, machine learning, LLM-based advisory generation, market price analysis, weather intelligence, voice interaction, multilingual UI, testing, and deployment support. The system helps farmers receive market and climate-based recommendations through a simple dashboard and voice-enabled interface.

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
