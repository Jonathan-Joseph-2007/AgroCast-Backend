<p align="center">
  <h1 align="center">🌾 AgroCast AI</h1>
  <p align="center"><strong>Smart Mandi Price & Logistics Advisory for Indian Farmers</strong></p>
  <p align="center">
    <a href="#features">Features</a> •
    <a href="#tech-stack">Tech Stack</a> •
    <a href="#setup">Setup</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#license">License</a>
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
  <sub>Built with ❤️ for Indian Farmers</sub>
</p>
