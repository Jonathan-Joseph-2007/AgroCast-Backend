import os
import uuid
import joblib
import random
import numpy as np
import asyncio
from dotenv import load_dotenv

# Load .env BEFORE anything else reads env vars
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from openai import AsyncOpenAI
from elevenlabs.client import AsyncElevenLabs
from elevenlabs import save
from fetcher import get_live_weather, get_live_aqi
from market_data import build_market_comparison, geocode_location

app = FastAPI(title="AgroCast Pipeline API")

# Setup CORS for Frontend Team (allow all for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory to serve audio files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Variables and Clients
FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")
FEATHERLESS_API_URL = "https://api.featherless.ai/v1"
FEATHERLESS_MODEL = "deepseek-ai/DeepSeek-V3-0324" 

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

featherless_client = AsyncOpenAI(
    api_key=FEATHERLESS_API_KEY,
    base_url=FEATHERLESS_API_URL,
)
elevenlabs_client = AsyncElevenLabs(
    api_key=ELEVENLABS_API_KEY
)

# Load ML Models cleanly at startup (environmental model still used for AQI forecasting)
print("Loading ML models...")
try:
    environmental_model = joblib.load("environmental_model.pkl")
    print("Successfully loaded environmental_model.pkl")
except FileNotFoundError as e:
    print(f"Warning: environmental_model.pkl not found. ({e})")
    environmental_model = None

# price_model is no longer needed — replaced by live data.gov.in API
price_model = None

class PredictionRequest(BaseModel):
    crop: str
    yield_amount: float
    current_price: float = 0.0
    distant_market_price: float = 0.0
    language: str = "Tamil"
    intent: str = "full_advice"
    location: Optional[str] = "Coimbatore"

@app.get("/health")
async def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "healthy", "models_loaded": environmental_model is not None}

@app.post("/predict")
async def predict(request: PredictionRequest):
    """
    Main prediction pipeline: Fetch real market data, forecast AQI, 
    generate bilingual text advisory, and synthesize speech audio.
    """
    location = request.location or "Coimbatore"
    
    # 1. Fetch Live Weather & AQI
    geo = geocode_location(location)
    lat, lon = geo["lat"], geo["lon"]
    weather_data = get_live_weather(lat, lon)
    aqi_data = get_live_aqi(lat, lon)
    
    current_temp = weather_data.get("temperature_celsius") or 25.0
    current_humidity = weather_data.get("relative_humidity_percent") or 50.0
    current_precip = weather_data.get("precipitation_mm") or 0.0

    # 2. Fetch Real Market Data (replaces the old price_model.pkl)
    market_comparison = build_market_comparison(
        user_location=location,
        crop=request.crop,
        yield_kg=request.yield_amount
    )
    
    local_market = market_comparison.get("local_market")
    nearby_markets = market_comparison.get("nearby_markets", [])
    best_market = market_comparison.get("best_market")
    
    # Extract key price data for the advisory
    if local_market:
        local_price_per_kg = local_market["price_per_kg"]
        local_revenue = local_market.get("total_revenue", local_price_per_kg * request.yield_amount)
    else:
        local_price_per_kg = request.current_price
        local_revenue = local_price_per_kg * request.yield_amount
    
    # Use accurate BEST PROFIT from the orchestrator
    profit_improvement = market_comparison.get("best_profit", 0)
    
    if best_market:
        best_price_per_kg = best_market["net_price_per_kg"]
        best_revenue = best_price_per_kg * request.yield_amount
        best_market_name = f"{best_market['market']} ({best_market['district']})"
        best_distance = best_market["distance_km"]
        best_transport_cost = best_market["transport_cost"]
    else:
        best_price_per_kg = local_price_per_kg
        best_revenue = local_revenue
        best_market_name = "N/A"
        best_distance = 0
        best_transport_cost = 0

    if profit_improvement > 2.0: # Only recommend transport if gain > Rs. 2 (to cover hidden hassles)
        recommended_action = "Transport to Distant Market"
    else:
        recommended_action = "Sell Locally"
        profit_improvement = 0 # Normalize to 0 if selling locally is better

    # 3. AQI Forecasting (environmental model still used)
    forecasted_aqi = 0.0
    if environmental_model is not None:
        env_inputs = np.array([[current_temp, current_humidity, current_precip]])
        forecasted_aqi = float(environmental_model.predict(env_inputs)[0])

    # 4. Build market summary for the AI prompt
    market_summary_lines = []
    for i, m in enumerate(nearby_markets[:5], 1):
        market_summary_lines.append(
            f"  {i}. {m['market']} ({m['district']}, {m['state']}): "
            f"₹{m['price_per_kg']}/kg, Distance: {m['distance_km']} km, "
            f"Transport: ₹{m['transport_cost']}, "
            f"Net profit vs local: ₹{m.get('profit_vs_local', 0)}"
        )
    market_summary = "\n".join(market_summary_lines) if market_summary_lines else "No nearby market data available."

    # 5. Explainability Layer (Featherless AI) — Bilingual Advisory
    if request.intent == "price_check":
        prompt = (
            f"Act as an agricultural market expert. A farmer at {location} is growing {request.crop}.\n"
            f"LOCAL MARKET DATA (from Government of India Mandi database):\n"
            f"  Local price: ₹{local_price_per_kg}/kg at {local_market['market'] if local_market else location}\n"
            f"  Local revenue for {request.yield_amount} kg: ₹{local_revenue:.0f}\n\n"
            f"NEARBY MARKETS:\n{market_summary}\n\n"
            f"BEST MARKET: {best_market_name} — Net ₹{best_price_per_kg}/kg after transport\n"
            f"PROFIT IMPROVEMENT: ₹{profit_improvement:.0f}\n"
            f"RECOMMENDED: {recommended_action}\n\n"
            f"INSTRUCTIONS:\n"
            f"- Write the advisory strictly in TWO sections.\n"
            f"- SECTION 1: Write entirely in {request.language} script. Give 2 short bullet points about the market data and recommendation.\n"
            f"- Then format a strict delimiter on its own line: ---\n"
            f"- SECTION 2: Below the delimiter, write the SAME advisory in English.\n"
            f"- Keep each section concise — max 3 bullet points each.\n"
            f"- Mention specific market names and prices.\n"
            f"- End every sentence with a full stop."
        )
    elif request.intent == "climate_check":
        prompt = (
            f"Act as an agricultural climate expert. A farmer at {location} is growing {request.crop}.\n"
            f"LIVE WEATHER: Temperature {current_temp}°C, Humidity {current_humidity}%, "
            f"Precipitation {current_precip} mm, AQI {aqi_data.get('aqi', 'N/A')}.\n"
            f"Forecasted AQI: {forecasted_aqi:.0f}\n\n"
            f"INSTRUCTIONS:\n"
            f"- Write the advisory strictly in TWO sections.\n"
            f"- SECTION 1: Write entirely in {request.language} script. Give 2 short bullet points about weather impact and recommendation.\n"
            f"- Then format a strict delimiter on its own line: ---\n"
            f"- SECTION 2: Below the delimiter, write the SAME advisory in English.\n"
            f"- Keep each section concise.\n"
            f"- End every sentence with a full stop."
        )
    else:
        prompt = (
            f"Act as an agricultural market and logistics expert. A farmer at {location} is growing {request.crop} "
            f"with an expected yield of {request.yield_amount} kg.\n\n"
            f"LOCAL MARKET DATA (from Government of India Mandi database):\n"
            f"  Local price: ₹{local_price_per_kg}/kg at {local_market['market'] if local_market else location}\n"
            f"  Local revenue: ₹{local_revenue:.0f}\n\n"
            f"NEARBY MARKETS WITH TRANSPORT ANALYSIS:\n{market_summary}\n\n"
            f"BEST MARKET: {best_market_name} — Net ₹{best_price_per_kg}/kg after transport "
            f"(Distance: {best_distance} km, Transport cost: ₹{best_transport_cost})\n"
            f"PROFIT IMPROVEMENT vs LOCAL: ₹{profit_improvement:.0f}\n"
            f"RECOMMENDED ACTION: {recommended_action}\n\n"
            f"LIVE WEATHER: {current_temp}°C, Humidity {current_humidity}%, AQI {aqi_data.get('aqi', 'N/A')}\n\n"
            f"INSTRUCTIONS:\n"
            f"- Write the advisory strictly in TWO sections.\n"
            f"- SECTION 1: Write entirely in {request.language} script. Give 3 short bullet points:\n"
            f"  Bullet 1: Current local market price and revenue.\n"
            f"  Bullet 2: Best nearby market with distance and transport cost.\n"
            f"  Bullet 3: Clear recommendation — sell locally or transport.\n"
            f"- Then format a strict delimiter on its own line: ---\n"
            f"- SECTION 2: Below the delimiter, write the SAME advisory in English.\n"
            f"- Keep each section concise and actionable.\n"
            f"- End every sentence with a full stop."
        )

    max_retries = 3
    advisory_text = "Advisory generation failed."
    for attempt in range(max_retries):
        try:
            response = await featherless_client.chat.completions.create(
                model=FEATHERLESS_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=400
            )
            advisory_text = response.choices[0].message.content.strip()
            break
        except Exception as e:
            if "429" in str(e) or "concurrency" in str(e).lower():
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 * (attempt + 1))
                    continue
            raise HTTPException(status_code=500, detail=f"Featherless AI API error: {str(e)}")

    # 6. Accessibility Layer (ElevenLabs)
    # Generate MP3 using eleven_multilingual_v2
    try:
        audio_stream = elevenlabs_client.text_to_speech.convert(
            text=advisory_text,
            voice_id="21m00Tcm4TlvDq8ikWAM", # Rachel voice ID
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        
        # Save to static folder
        filename = f"advisory_{uuid.uuid4().hex[:8]}.mp3"
        filepath = os.path.join("static", filename)
        
        # Async Elevenlabs generate returns an async generator
        with open(filepath, "wb") as f:
            async for chunk in audio_stream:
                f.write(chunk)
                
        audio_url = f"/static/{filename}"
                
    except Exception as e:
        # If elevenlabs fails (e.g., missing API key), fallback gently
        print(f"ElevenLabs Audio Generation Error: {e}")
        audio_url = None

    # 7. Final Output — enriched with market comparison data
    return {
        "input_data": {
            "crop": request.crop,
            "location": location,
            "yield_amount": request.yield_amount,
        },
        "live_climate": {
            "temperature_celsius": current_temp,
            "relative_humidity_percent": current_humidity,
            "precipitation_mm": current_precip,
            "current_aqi": aqi_data.get("aqi")
        },
        "forecasts": {
            "forecasted_aqi": round(forecasted_aqi, 2),
            "profit_improvement": round(profit_improvement, 2),
            "recommended_action": recommended_action
        },
        "market_data": {
            "local_market": {
                "market_name": local_market["market"] if local_market else "Unknown",
                "district": local_market["district"] if local_market else location,
                "price_per_kg": local_price_per_kg,
                "min_price_quintal": local_market["min_price"] if local_market else 0,
                "max_price_quintal": local_market["max_price"] if local_market else 0,
                "total_revenue": round(local_revenue, 2),
            } if local_market else None,
            "nearby_markets": [
                {
                    "market_name": m["market"],
                    "district": m["district"],
                    "state": m["state"],
                    "price_per_kg": m["price_per_kg"],
                    "distance_km": m["distance_km"],
                    "drive_hours": m["drive_hours"],
                    "transport_cost": m["transport_cost"],
                    "transport_cost_per_kg": m["transport_cost_per_kg"],
                    "net_price_per_kg": m["net_price_per_kg"],
                    "profit_vs_local": m.get("profit_vs_local", 0),
                }
                for m in nearby_markets
            ],
            "best_market": {
                "market_name": best_market["market"] if best_market else "N/A",
                "district": best_market["district"] if best_market else "N/A",
                "net_price_per_kg": best_price_per_kg,
                "distance_km": best_distance,
                "transport_cost": best_transport_cost,
                "profit_improvement": round(profit_improvement, 2),
            } if best_market else None,
            "total_markets_found": market_comparison.get("total_markets_found", 0),
            "data_source": "Government of India — data.gov.in (Agmarknet)"
        },
        "advisory": advisory_text,
        "audio_url": audio_url
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
