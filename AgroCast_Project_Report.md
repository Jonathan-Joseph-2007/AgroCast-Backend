# AgroCast Market Intelligence System
**Project Overview & Technical Architecture Report**

## 1. Project Summary
AgroCast is an advanced, AI-driven agricultural market intelligence platform designed to empower local farmers by providing real-time, actionable insights. By replacing outdated static models with real-time data pipelines, the system acts as a bilingual "Smart Advisor." It allows a user to speak a natural language query in their regional dialect (e.g., *"Coimbatore mein tamatar ka kya price chal raha hai?"*). The system instantly parses the audio, geolocates the user, fetches live government market data, calculates exact transportation logistics using real road networks, and uses a generative LLM to provide a final spoken and written recommendation on the exact APMC market that maximizes the farmer's net profit.

---

## 2. Core Modules & Functionality
### A. Intelligent Voice Interface & NLP Pipeline
*   **Voice Input & Translation:** Users input their queries naturally using voice. 
*   **Entity Extraction (NER):** A strict LLM prompt extracts the core intent: the Crop (standardized to English), Location (resolved), requested Language, and estimated Yield.
*   **Bilingual Generation:** The final market advisory is dynamically generated in both the requested Regional Language (Tamil, Hindi, Malayalam, Telugu) and English.
*   **Text-to-Speech (TTS):** The regional advisory is converted into native-sounding spoken audio so illiterate or purely regional-speaking farmers can listen to the insights instantly.

### B. Live Data & Market Intelligence Engine
*   **Government API Integration:** Direct integration with the **data.gov.in (Agmarknet)** API to fetch real-time Daily Mandi Prices specific to the requested crop and geographical state.
*   **Smart Fallback Synthesizer:** If the Government API undergoes maintenance or rotates tokens (returning 0 records), a fallback mathematical module automatically kicks in. It realistically simulates APMC market prices and variance across the user's nearest districts to ensure 100% uptime for presentations.
*   **Live Environmental Data:** Connects to forecasting networks to pull exact current Temperature (°C), Humidity, Precipitation (mm), and European Standard Air Quality Index (AQI) based on the user's geolocation.

### C. Geospatial & Logistics Routing
*   **Dual-Pass Resolution Algorithm:** 
    1.  *Haversine Estimation:* Quickly filters the entire Indian map to pinpoint the top 5 closest districts radially from the user's coordinates.
    2.  *Real-World Routing:* Sends the top candidates directly to a routing engine to calculate physical road driving distances (km) and driving durations (hours).
*   **Dynamic Logistics Calculation:** Calculates transportation costs dynamically using truck base-fares, distance multipliers, and yield-weight constraints to output the **Net Profit per kg**.

### D. Premium Intelligent UI Dashboard
*   **Glassmorphism User Interface:** A dark-themed, ultra-modern dashboard visualizing the intelligence pipeline.
*   **Comparison Cards:** Renders side-by-side metric cards to compare the Local Market against the "Best Distant Market". Features live visual price-bars.
*   **Localized Price Tables:** A dynamically translating data grid that maps column headers (Market, Distance, Transport Cost, Profit) instantly into the user's requested regional language.

---

## 3. Technology Stack List
Here is the strict technological architecture required to run and deploy AgroCast:

### Frontend Layer
*   **Streamlit:** Core web application framework for building the reactive dashboard UI.
*   **Custom Vanilla CSS/HTML:** Extensive UI injections to create the Glassmorphism styling, metrics pills, best-market badges, and custom grid alignments.
*   **audio_recorder_streamlit:** Component used to interface with the web browser's microphone API for live voice capture.
*   **Pandas:** Used strictly for DataFrame management to render the Price Comparison Tables seamlessly.

### Backend Application Layer
*   **FastAPI:** High-performance, asynchronous REST API framework serving the core `/predict` pipeline linking the UI to the AI tools.
*   **Python 3.10+:** The foundational scripting language managing the complete backend lifecycle.
*   **Uvicorn:** The ASGI web server used to run the FastAPI application efficiently on `localhost:8000`.

### Geospatial & Logistics Engines
*   **Geopy (Nominatim API):** The geocoding engine utilized to convert string names ("Coimbatore") into raw decimal Geographic Coordinates (Latitude, Longitude).
*   **OSRM (Open Source Routing Machine API):** The logistical backend used over HTTP to track physical road networks instead of "as the crow flies" distances.
*   **Math Module:** Utilized for native spherical Haversine formula processing within the fallback sorting algorithms.

### Artificial Intelligence & Third-Party APIs
*   **Featherless AI:** The core Large Language Model (LLM) provider utilized for the massive Entity Extraction and Bilingual Market Advisory Generation. (Utilizes the `openai` Python SDK wrapper).
*   **ElevenLabs API:** State-of-the-art neural audio generation pipeline utilized to generate the regional Text-to-Speech (TTS) bytes.
*   **Open-Meteo API:** Used for exact weather and climate polling.
*   **Data.gov.in API:** The Indian Government portal for real-time agricultural APMC polling.

### Execution Hooks
*   **PowerShell / Shell Scripts (`run_all.ps1`):** Execution orchestrator designed to spawn multi-threaded terminal windows allowing the Frontend and Backend processes to run synchronously and independently on local test platforms.
