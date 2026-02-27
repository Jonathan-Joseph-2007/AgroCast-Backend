import os
import uuid
import json
import re
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from twilio.twiml.voice_response import VoiceResponse, Gather
from gtts import gTTS

# --- STRICT RULE: Isolated Import Logic ---
# Importing ML models, DeepSeek AI client, and core prediction logic from main.py
# This ensures zero modifications or breaking changes to the existing app.py or main.py.
from main import (
    featherless_client, 
    FEATHERLESS_MODEL, 
    environmental_model, 
    price_model, 
    predict, 
    PredictionRequest
)

# Start new background server on custom port 8001
app_voice = FastAPI(title="AgroCast Twilio Microservice")

# Static mounting for serving the gTTS output safely over public URLs to Twilio
os.makedirs("twilio_static", exist_ok=True)
app_voice.mount("/static", StaticFiles(directory="twilio_static"), name="static")

LANG_MAP = {
    "1": "Hindi",
    "2": "Tamil",
    "3": "Malayalam",
    "4": "Telugu"
}

GTTS_MAP = {
    "Hindi": "hi",
    "Tamil": "ta",
    "Malayalam": "ml",
    "Telugu": "te",
    "English": "en"
}

def clean_text(text):
    """The protected unicode speech cleaner borrowed from app.py"""
    text = text.replace('₹', 'Rupees').replace('/kg', 'per kilogram')
    text = text.replace('Rs.', 'Rupees').replace('Rs', 'Rupees')
    clean_pattern = r'[^\w\s\.\u0900-\u097F\u0B80-\u0BFF\u0C00-\u0C7F\u0D00-\u0D7F]'
    return re.sub(clean_pattern, ' ', text).strip()

@app_voice.get("/health")
async def health_check():
    """Simple health check to verify local deployment is working before Ngrok."""
    return {"status": "ready", "service": "Twilio Voice IVR Microservice"}

@app_voice.post("/voice/incoming")
async def voice_incoming(request: Request):
    """Initial Twilio Webhook parsing digits for language"""
    print("\n[IVR LOG] 📞 Incoming Call Detected!")
    response = VoiceResponse()
    
    gather = Gather(num_digits=1, action="/voice/ask", timeout=5)
    # Give instructions in fallback English voice for button presses
    gather.say("Welcome to Agro Cast AI. Press 1 for Hindi. Press 2 for Tamil. Press 3 for Malayalam. Press 4 for Telugu.")
    response.append(gather)
    
    response.say("We did not receive any input. Goodbye.")
    return HTMLResponse(content=str(response), media_type="application/xml")

@app_voice.post("/voice/ask")
async def voice_ask(request: Request, Digits: str = Form(None)):
    """Acknowledge dialect and ask for the farm question via Gather input='speech'"""
    response = VoiceResponse()
    
    selected_language = LANG_MAP.get(Digits, "English")
    
    # Translated Prompts
    prompts = {
        "Hindi": "कृपया बीप के बाद अपनी फसल और बाजार का प्रश्न बताएं।",
        "Tamil": "பீப் ஒலிக்குப் பிறகு உங்கள் பயிர் மற்றும் சந்தைக் கேள்வியைக் கூறவும்.",
        "Malayalam": "ബീപ്പിന് ശേഷം നിങ്ങളുടെ വിള, വിപണി ചോദ്യം പറയുക.",
        "Telugu": "బీప్ తర్వాత మీ పంట మరియు మార్కెట్ ప్రశ్నను తెలపండి.",
        "English": "Please state your crop and market question after the beep."
    }
    
    ack_text = prompts.get(selected_language)
    clean_ack = clean_text(ack_text)
    gtts_code = GTTS_MAP.get(selected_language, "en")
    
    # Use gTTS to dynamically save and <Play> the greeting so native accents are flawless
    tts = gTTS(text=clean_ack, lang=gtts_code)
    filename = f"ask_{uuid.uuid4().hex[:8]}.mp3"
    filepath = os.path.join("twilio_static", filename)
    tts.save(filepath)
    
    base_url = str(request.base_url).rstrip("/")
    audio_url = f"{base_url}/static/{filename}"
    
    tw_lang = "hi-IN" if selected_language == "Hindi" else "en-IN"
    
    gather = Gather(input="speech", action=f"/voice/process?lang={selected_language}", timeout=5, language=tw_lang)
    gather.play(audio_url)
    
    response.append(gather)
    response.say("Sorry, I didn't catch that. Good bye.")
    
    return HTMLResponse(content=str(response), media_type="application/xml")

@app_voice.post("/voice/process")
async def voice_process(request: Request, SpeechResult: str = Form(None), lang: str = "English"):
    """Isolate the Speech text, extract with Featherless, route to Main Predictor, synthesize audio"""
    response = VoiceResponse()
    
    if not SpeechResult:
        response.say("No speech detected.")
        response.hangup()
        return HTMLResponse(content=str(response), media_type="application/xml")
        
    print(f"\n[IVR LOG] 🎙️ Speech Transcription Received: '{SpeechResult}'")
    print(f"[IVR LOG] 🌐 Target Dialect: {lang}")
    
    # Step 1: Data Extraction System mapped from the frontend logic
    system_prompt = (
        f"You are a Strict Data Extractor. Analyze the user's voice text and output ONLY a JSON.\n"
        f"The user selected {lang}. You MUST output the \"advisory\" text strictly using the {lang} script.\n"
        f"CRITICAL RULES: Absolutely NO English letters allowed in advisory field.\n"
        "Identify the intent:\n"
        "- If price related, intent = 'price_check'.\n"
        "- If climate/weather related, intent = 'climate_check'.\n"
        "- If selling, intent = 'full_advice'.\n"
        "- If off-topic (politics, movies), intent = 'off_topic'.\n\n"
        "Extract 'crop' and map it to English (e.g., Aalu -> Potato). Extract numbers.\n"
        "Defaults if missing: yield_amount: 2500, current_price: 40, distant_market_price: 55.\n"
        "Keys: intent, language, crop, yield_amount, current_price, distant_market_price."
    )
    
    try:
        extraction_res = await featherless_client.chat.completions.create(
            model=FEATHERLESS_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": SpeechResult}
            ]
        )
        extraction_str = extraction_res.choices[0].message.content.strip()
        if extraction_str.startswith("```json"):
            extraction_str = extraction_str[7:-3].strip()
        elif extraction_str.startswith("```"):
            extraction_str = extraction_str[3:-3].strip()
            
        payload = json.loads(extraction_str)
        
        # Step 2: Safety bypass & routing
        if payload.get("intent") == "off_topic":
            advisory_text = "I can only assist with agricultural questions. This interaction will now end."
            final_lang = "English"
        else:
            # Step 3: Pass seamlessly to the ML backend (imported safely)
            req = PredictionRequest(
                crop=payload.get("crop", "Tomato"),
                yield_amount=payload.get("yield_amount", 2500.0),
                current_price=payload.get("current_price", 40.0),
                distant_market_price=payload.get("distant_market_price", 55.0),
                language=lang,
                intent=payload.get("intent", "full_advice")
            )
            
            # Predict heavily relies on loaded 'environmental_model.pkl' & 'price_model.pkl'
            main_response = await predict(req)
            advisory_text = main_response["advisory"]
            final_lang = lang
            print(f"[IVR LOG] 🧠 ML Advisory Generated: {advisory_text}")
            
        # Step 4: Stream Audio Back
        clean_adv = clean_text(advisory_text)
        gtts_code = GTTS_MAP.get(final_lang, "en")
        
        tts = gTTS(text=clean_adv, lang=gtts_code)
        filename = f"ivr_{uuid.uuid4().hex[:8]}.mp3"
        filepath = os.path.join("twilio_static", filename)
        tts.save(filepath)
        
        base_url = str(request.base_url).rstrip("/")
        audio_url = f"{base_url}/static/{filename}"
        
        response.play(audio_url)
        response.hangup()
        
    except Exception as e:
        print(f"Twilio Endpoint Error: {e}")
        response.say("I am having trouble processing your request over the phone network.")
        response.hangup()
        
    return HTMLResponse(content=str(response), media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("twilio_server:app_voice", host="0.0.0.0", port=8001, reload=True)
