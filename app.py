import streamlit as st
import requests
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from gtts import gTTS
import tempfile
import time
import re
import pandas as pd

st.set_page_config(
    page_title="AgroCast AI — Smart Mandi Advisory",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Premium Dark Agri-Tech CSS ──────────────────────────────────────────────
st.markdown("""
<style>
/* ─── Google Font Import ─── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─── Global Reset & Background ─── */
.stApp {
    background: linear-gradient(145deg, #0a1a0f 0%, #0d1f12 30%, #111e16 60%, #0e1a11 100%);
    font-family: 'Inter', sans-serif;
}

/* ─── Hide Streamlit defaults ─── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ─── Global Text ─── */
p, span, label, div, li {
    color: #c8e6c9 !important;
    font-family: 'Inter', sans-serif !important;
}

h1, h2, h3, h4 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
}

/* ─── Hero Header ─── */
.hero-container {
    text-align: center;
    padding: 2rem 1rem 1rem;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #66bb6a 0%, #aed581 40%, #dce775 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: #8d9e8f !important;
    font-weight: 400;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(46, 125, 50, 0.2);
    border: 1px solid rgba(76, 175, 80, 0.3);
    border-radius: 20px;
    padding: 4px 16px;
    font-size: 0.75rem;
    color: #81c784 !important;
    margin-top: 0.5rem;
    letter-spacing: 1px;
}

/* ─── Glass Cards ─── */
.glass-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.glass-card:hover {
    border-color: rgba(76, 175, 80, 0.3);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 0 20px rgba(76,175,80,0.05);
    transform: translateY(-2px);
}

/* ─── Market Card ─── */
.market-card {
    background: linear-gradient(135deg, rgba(27,94,32,0.15) 0%, rgba(0,0,0,0.3) 100%);
    border: 1px solid rgba(76,175,80,0.15);
    border-radius: 14px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
.market-card:hover {
    border-color: rgba(76,175,80,0.4);
    transform: translateY(-1px);
}
.market-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #2e7d32, #66bb6a, #aed581);
}

.market-name {
    font-size: 1rem;
    font-weight: 700;
    color: #e8f5e9 !important;
    margin-bottom: 0.3rem;
}
.market-district {
    font-size: 0.8rem;
    color: #81c784 !important;
    margin-bottom: 0.8rem;
}

/* ─── Price Tags ─── */
.price-tag {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.5rem;
    font-weight: 700;
    color: #66bb6a !important;
}
.price-unit {
    font-size: 0.75rem;
    color: #8d9e8f !important;
    font-weight: 400;
}

/* ─── Metric Pills ─── */
.metric-pill {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(255,255,255,0.05);
    border-radius: 8px;
    padding: 4px 10px;
    font-size: 0.78rem;
    margin: 2px 4px 2px 0;
    color: #a5d6a7 !important;
}
.metric-pill.distance { border-left: 3px solid #42a5f5; }
.metric-pill.time { border-left: 3px solid #ffb74d; }
.metric-pill.cost { border-left: 3px solid #ef5350; }
.metric-pill.profit-up { border-left: 3px solid #66bb6a; color: #66bb6a !important; }
.metric-pill.profit-down { border-left: 3px solid #ef5350; color: #ef5350 !important; }

/* ─── Best Market Glow ─── */
.best-market {
    border-color: rgba(102, 187, 106, 0.4) !important;
    box-shadow: 0 0 20px rgba(102, 187, 106, 0.1);
}
.best-market::before {
    background: linear-gradient(90deg, #66bb6a, #aed581, #66bb6a) !important;
    height: 4px !important;
}
.best-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background: linear-gradient(135deg, #2e7d32, #43a047);
    color: #fff !important;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 10px;
    letter-spacing: 0.5px;
}

/* ─── Advisory Cards ─── */
.advisory-regional {
    background: linear-gradient(135deg, rgba(27,94,32,0.25) 0%, rgba(0,0,0,0.3) 100%);
    border: 1px solid rgba(76,175,80,0.2);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border-left: 4px solid #66bb6a;
}
.advisory-english {
    background: linear-gradient(135deg, rgba(33,150,243,0.08) 0%, rgba(0,0,0,0.2) 100%);
    border: 1px solid rgba(33,150,243,0.15);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border-left: 4px solid #42a5f5;
}
.advisory-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.7rem;
}
.advisory-text {
    font-size: 1rem;
    line-height: 1.7;
    color: #e0e0e0 !important;
}

/* ─── Language Selector Buttons ─── */
.stButton>button {
    background: linear-gradient(135deg, rgba(46,125,50,0.3) 0%, rgba(27,94,32,0.5) 100%) !important;
    color: #e8f5e9 !important;
    font-weight: 600;
    border-radius: 12px;
    border: 1px solid rgba(76,175,80,0.25) !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    transition: all 0.3s ease !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.5rem 1rem;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #2e7d32 0%, #388e3c 100%) !important;
    color: #ffffff !important;
    border-color: #4caf50 !important;
    box-shadow: 0 6px 20px rgba(46,125,50,0.4) !important;
    transform: translateY(-2px);
}

/* ─── Info/Success/Warning boxes ─── */
div[data-baseweb="notification"] {
    background: rgba(27,94,32,0.2) !important;
    border: 1px solid rgba(76,175,80,0.2) !important;
    border-radius: 12px !important;
    border-left: 4px solid #66bb6a !important;
}
div[data-baseweb="notification"] p {
    color: #e8f5e9 !important;
}

/* ─── Data Table Styling ─── */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
}

/* ─── Divider ─── */
hr {
    border-color: rgba(76,175,80,0.15) !important;
    margin: 1.5rem 0;
}

/* ─── Section Headers ─── */
.section-header {
    font-size: 1.3rem;
    font-weight: 700;
    color: #81c784 !important;
    margin: 1.5rem 0 0.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ─── Price Comparison Bar ─── */
.price-bar-container {
    background: rgba(255,255,255,0.03);
    border-radius: 8px;
    height: 28px;
    overflow: hidden;
    margin: 4px 0;
    position: relative;
}
.price-bar {
    height: 100%;
    border-radius: 8px;
    display: flex;
    align-items: center;
    padding-left: 10px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #fff !important;
    transition: width 0.8s ease;
}
.price-bar.local { background: linear-gradient(90deg, #1b5e20, #2e7d32); }
.price-bar.market { background: linear-gradient(90deg, #0d47a1, #1565c0); }
.price-bar.best { background: linear-gradient(90deg, #e65100, #f57c00); }

/* ─── Pulse animation for recording ─── */
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(76,175,80,0.4); }
    70% { box-shadow: 0 0 0 15px rgba(76,175,80,0); }
    100% { box-shadow: 0 0 0 0 rgba(76,175,80,0); }
}

/* ─── Data source badge ─── */
.data-source {
    text-align: center;
    font-size: 0.7rem;
    color: #6b7c6d !important;
    padding: 0.5rem;
    margin-top: 1rem;
    border-top: 1px solid rgba(76,175,80,0.1);
}
</style>
""", unsafe_allow_html=True)

LANG_CODES = {'Tamil': 'ta', 'Hindi': 'hi', 'Malayalam': 'ml', 'Telugu': 'te'}

def clean_text_for_speech(text):
    # 1. First, replace technical symbols with actual words so they make sense aloud
    text = text.replace('₹', 'Rupees').replace('/kg', 'per kilogram')
    text = text.replace('Rs.', 'Rupees').replace('Rs', 'Rupees')
    
    # 2. DELETE only specific unwanted symbols like ( ) [ ] : _ *
    # We use a 'negated set' that PRESERVES letters, numbers, spaces, and ALL Indian scripts
    # Pattern: [^\w\s\.\u0900-\u097F\u0B80-\u0BFF\u0C00-\u0C7F\u0D00-\u0D7F]
    clean_pattern = r'[^\w\s\.\u0900-\u097F\u0B80-\u0BFF\u0C00-\u0C7F\u0D00-\u0D7F]'
    text = re.sub(clean_pattern, ' ', text)
    
    # 3. Clean up extra spaces so gTTS doesn't pause too long
    return re.sub(r'\s+', ' ', text).strip()

@st.cache_resource
def get_openai_client():
    load_dotenv()
    return OpenAI(
        base_url="https://api.featherless.ai/v1",
        api_key=os.getenv('FEATHERLESS_API_KEY', '')
    )

client = get_openai_client()

# ─── Hero Header ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🌾 AgroCast AI</div>
    <div class="hero-subtitle">Smart Mandi Price & Logistics Advisory</div>
    <div class="hero-badge">⚡ Powered by Government of India Mandi Data</div>
</div>
""", unsafe_allow_html=True)

# ─── Language Selection ──────────────────────────────────────────────────────
if 'target_lang' not in st.session_state:
    st.session_state.target_lang = "Tamil"

LANGUAGE_UI_MAP = {
    'தமிழ்': 'Tamil',
    'हिन्दी': 'Hindi',
    'മലയാളം': 'Malayalam',
    'తెలుగు': 'Telugu'
}

col_spacer_l, col_lang, col_spacer_r = st.columns([1, 3, 1])
with col_lang:
    lang_cols = st.columns(4)
    for i, (native_script, english_name) in enumerate(LANGUAGE_UI_MAP.items()):
        if lang_cols[i].button(native_script, use_container_width=True, key=f"lang_{english_name}"):
            st.session_state.target_lang = english_name

current_native = next((k for k, v in LANGUAGE_UI_MAP.items() if v == st.session_state.target_lang), st.session_state.target_lang)
st.markdown(f"""
<div style="text-align:center; margin: 0.5rem 0 1rem;">
    <span class="metric-pill" style="font-size:0.85rem; padding:6px 16px;">
        🌐 {current_native} — {st.session_state.target_lang}
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─── UI Translations ─────────────────────────────────────────────────────────
UI_TRANSLATIONS = {
    "English": {
        "instruction": "🎙️ Click the microphone and ask about your crop & location:",
        "mic_label": "Click to record",
        "processing": "Analyzing markets...",
        "you_said": "You said:",
    },
    "Tamil": {
        "instruction": "🎙️ மைக்ரோஃபோனைக் கிளிக் செய்து உங்கள் பயிர் & இடம் பற்றி கேளுங்கள்:",
        "mic_label": "பதிவு செய்ய கிளிக் செய்யவும்",
        "processing": "சந்தைகளை பகுப்பாய்வு செய்கிறது...",
        "you_said": "நீங்கள் கூறியது:",
    },
    "Hindi": {
        "instruction": "🎙️ माइक्रोफ़ोन पर क्लिक करें और अपनी फसल और स्थान के बारे में पूछें:",
        "mic_label": "रिकॉर्ड करने के लिए क्लिक करें",
        "processing": "बाज़ारों का विश्लेषण...",
        "you_said": "आपने कहा:",
    },
    "Malayalam": {
        "instruction": "🎙️ മൈക്രോഫോണിൽ ക്ലിക്കുചെയ്ത് നിങ്ങളുടെ വിളയെയും സ്ഥലത്തെയും കുറിച്ച് ചോദിക്കുക:",
        "mic_label": "റെക്കോർഡുചെയ്യാൻ ക്ലിക്കുചെയ്യുക",
        "processing": "വിപണികൾ വിശകലനം ചെയ്യുന്നു...",
        "you_said": "നിങ്ങൾ പറഞ്ഞത്:",
    },
    "Telugu": {
        "instruction": "🎙️ మైక్రోఫోన్‌పై క్లిక్ చేసి మీ పంట & ప్రదేశం గురించి అడగండి:",
        "mic_label": "రికార్డ్ చేయడానికి క్లిక్ చేయండి",
        "processing": "మార్కెట్లను విశ్లేషిస్తోంది...",
        "you_said": "మీరు చెప్పింది:",
    }
}

ui_text = UI_TRANSLATIONS.get(st.session_state.target_lang, UI_TRANSLATIONS["English"])

# ─── Voice Input ─────────────────────────────────────────────────────────────
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    st.markdown(f"<p style='text-align:center; font-size:1rem;'>{ui_text['instruction']}</p>", unsafe_allow_html=True)
    audio_bytes = audio_recorder(text=ui_text["mic_label"])

# ─── Processing Pipeline ─────────────────────────────────────────────────────
if audio_bytes:
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes)
        
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile("temp.wav") as source:
            audio_data = recognizer.record(source)
            user_text = recognizer.recognize_google(audio_data)
            
        st.info(f"**{ui_text['you_said']}** {user_text}")
        
        with st.spinner(ui_text['processing']):
            # --- 1. INTENT GUARDRAIL (THE JUDGE) ---
            weather_keywords = ['mausam', 'weather', 'aqi', 'climate', 'temperature', 'humidity', 'rain', 'monsoon']
            is_weather = any(wk in user_text.lower() for wk in weather_keywords)
            
            if is_weather:
                judge_decision = "YES"
            else:
                judge_prompt = (
                    "You are an expert in Indian Agriculture. The user is asking about crops using regional names "
                    "(like Aalu for Potato, Vengayam for Onion). If the text mentions ANY vegetable, fruit, grain, "
                    "or market price in any Indian language, answer 'YES'. Text: " + user_text
                )
                judge_res = client.chat.completions.create(
                    model="deepseek-ai/DeepSeek-V3-0324",
                    messages=[{"role": "user", "content": judge_prompt}],
                    temperature=0
                )
                judge_decision = judge_res.choices[0].message.content.strip().upper()
                
            if "YES" not in judge_decision:
                rejection_messages = {
                    'Tamil': 'மன்னிக்கவும், இது விவசாயம் தொடர்பான கேள்வி அல்ல. தயவுசெய்து பயிர்கள் அல்லது விலைகள் பற்றி கேட்கவும்.',
                    'Hindi': 'क्षमा करें, यह कृषि से संबंधित प्रश्न नहीं है। कृपया फसलों या कीमतों के बारे में पूछें।',
                    'Telugu': 'క్షమించండి, ఇది వ్యవసాయానికి సంబంధించిన ప్రశ్న కాదు. దయచేసి పంటలు లేదా ధరల గురించి అడగండి.',
                    'Malayalam': 'ക്ഷമിക്കണം, ഇത് കൃഷിയുമായി ബന്ധപ്പെട്ട ചോദ്യമല്ല. ദയവായി വിളകളെക്കുറിച്ചോ വിലകളെക്കുറിച്ചോ ചോദിക്കുക.',
                    'English': 'I can only assist with agricultural questions.'
                }
                advisory_text = rejection_messages.get(st.session_state.target_lang, "I can only assist with agricultural questions.")
                st.warning(advisory_text)
                
                lang_codes = {'Hindi': 'hi', 'Tamil': 'ta', 'Malayalam': 'ml', 'Telugu': 'te', 'English': 'en'}
                current_code = lang_codes.get(st.session_state.target_lang, 'en')
                clean_text = clean_text_for_speech(advisory_text)
                tts = gTTS(text=clean_text, lang=current_code, slow=False)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                tts.save(temp_file.name)
                time.sleep(1)
                st.audio(temp_file.name, format="audio/mp3", autoplay=True)
                st.stop()
                
            # --- 2. DATA EXTRACTION (now also extracts location) ---
            system_prompt = (
                f"You are a Strict Data Extractor. Analyze the user's voice text and output ONLY a JSON.\n\n"
                f"You are a strict native agricultural translator. The user has selected {st.session_state.target_lang}.\n"
                f"CRITICAL RULES FOR THE \"advisory\" FIELD:\n"
                f"- It MUST be written 100% in the native {st.session_state.target_lang} script.\n"
                f"- ABSOLUTELY NO English letters (A-Z, a-z) are allowed in the advisory text.\n"
                f"- Translate all technical terms (Profit, Yield, AQI, Weather, Market) into pure {st.session_state.target_lang}.\n"
                f"- Do not use transliterated English.\n\n"
                "Identify the intent:\n"
                "- If the user asks about price, intent = 'price_check'.\n"
                "- If they ask about weather/climate, intent = 'climate_check'.\n"
                "- If they ask about selling/market, intent = 'full_advice'.\n\n"
                "Extract the CROP and map regional names to STANDARD ENGLISH (e.g. 'Tamatar' -> 'Tomato', 'Vengayam' -> 'Onion').\n"
                "Extract the LOCATION/PLACE/CITY if mentioned (e.g. 'Coimbatore', 'Pollachi'). Map to standard English name without states.\n"
                "If absolutely no location is mentioned anywhere, use 'Coimbatore'.\n\n"
                "Validation: If no crop is clearly mentioned, use 'Tomato'.\n\n"
                "Output JSON keys exactly: intent, language, crop, yield_amount (default 2500), current_price (default 40), distant_market_price (default 55), location."
            )
            
            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3-0324",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ]
            )
            
            # Parse the JSON response
            extraction_str = response.choices[0].message.content.strip()
            if extraction_str.startswith("```json"):
                extraction_str = extraction_str[7:-3].strip()
            elif extraction_str.startswith("```"):
                extraction_str = extraction_str[3:-3].strip()
                
            payload = json.loads(extraction_str)
            
            # Ensure location is in payload
            if "location" not in payload or not payload["location"]:
                payload["location"] = "Coimbatore"
            
            # --- 3. BACKEND API CALL ---
            API_URL = "http://localhost:8000/predict"
            time.sleep(2.5)
            api_response = requests.post(API_URL, json=payload, timeout=60)
            
            if api_response.status_code == 200:
                data = api_response.json()
                
                advisory_text = data.get("advisory", "No advice generated.")
                market_data = data.get("market_data", {})
                local_market = market_data.get("local_market")
                nearby_markets = market_data.get("nearby_markets", [])
                best_market_info = market_data.get("best_market")
                forecasts = data.get("forecasts", {})
                climate = data.get("live_climate", {})
                input_data = data.get("input_data", {})
                
                # ═══════════════════════════════════════════════════════════
                # VISUAL OUTPUT — MARKET COMPARISON DASHBOARD
                # ═══════════════════════════════════════════════════════════
                
                st.markdown("---")
                
                # ─── Top Stats Row ────────────────────────────────────────
                st.markdown('<div class="section-header">📊 Market Intelligence Dashboard</div>', unsafe_allow_html=True)
                
                stat_cols = st.columns(4)
                with stat_cols[0]:
                    st.markdown(f"""<div class="glass-card" style="text-align:center;">
<div style="font-size:0.75rem; color:#8d9e8f !important; text-transform:uppercase; letter-spacing:1px;">Crop</div>
<div style="font-size:1.4rem; font-weight:700; color:#aed581 !important;">🌿 {input_data.get('crop', 'N/A')}</div>
<div style="font-size:0.8rem; color:#81c784 !important; font-weight:600; margin-top:2px;">Avg Price: ₹{local_market['price_per_kg'] if local_market else 'N/A'}/kg</div>
</div>""", unsafe_allow_html=True)
                with stat_cols[1]:
                    st.markdown(f"""<div class="glass-card" style="text-align:center;">
<div style="font-size:0.75rem; color:#8d9e8f !important; text-transform:uppercase; letter-spacing:1px;">Location</div>
<div style="font-size:1.4rem; font-weight:700; color:#81c784 !important;">📍 {input_data.get('location', 'N/A')}</div>
</div>""", unsafe_allow_html=True)
                with stat_cols[2]:
                    st.markdown(f"""<div class="glass-card" style="text-align:center;">
<div style="font-size:0.75rem; color:#8d9e8f !important; text-transform:uppercase; letter-spacing:1px;">Markets Found</div>
<div style="font-size:1.4rem; font-weight:700; color:#42a5f5 !important;">🏪 {market_data.get('total_markets_found', 0)}</div>
</div>""", unsafe_allow_html=True)
                with stat_cols[3]:
                    # Profit Gain logic
                    profit = forecasts.get("profit_improvement", 0)
                    if profit > 10:
                        profit_color = "#66bb6a" # Green for gain
                        profit_icon = "📈"
                        profit_text = f"+₹{profit:,.0f}"
                    elif profit < -10:
                        profit_color = "#ef5350" # Red for loss
                        profit_icon = "📉"
                        profit_text = f"₹{profit:,.0f}"
                    else:
                        profit_color = "#42a5f5" # Blue for neutral/local best
                        profit_icon = "⚖️"
                        profit_text = "Sell Local"

                    st.markdown(f"""<div class="glass-card" style="text-align:center;">
<div style="font-size:0.75rem; color:#8d9e8f !important; text-transform:uppercase; letter-spacing:1px;">Best Profit Gain</div>
<div style="font-size:1.4rem; font-weight:700; color:{profit_color} !important;">{profit_icon} {profit_text}</div>
</div>""", unsafe_allow_html=True)

                # ─── Local Market Card ────────────────────────────────────
                if local_market:
                    st.markdown('<div class="section-header">🏠 Your Local Market</div>', unsafe_allow_html=True)
                    
                    lm_col1, lm_col2, lm_col3 = st.columns([2, 1, 1])
                    with lm_col1:
                        st.markdown(f"""<div class="market-card">
<div class="market-name">{local_market['market_name']}</div>
<div class="market-district">📍 {local_market['district']}</div>
<div class="price-tag">₹{local_market['price_per_kg']}<span class="price-unit"> /kg</span></div>
</div>""", unsafe_allow_html=True)
                    with lm_col2:
                        st.markdown(f"""<div class="glass-card" style="text-align:center;">
<div style="font-size:0.7rem; color:#8d9e8f !important; text-transform:uppercase;">Min Price</div>
<div style="font-size:1.2rem; font-weight:600; color:#ef5350 !important;">₹{local_market.get('min_price_quintal',0)}</div>
<div style="font-size:0.65rem; color:#6b7c6d !important;">per quintal</div>
</div>""", unsafe_allow_html=True)
                    with lm_col3:
                        st.markdown(f"""<div class="glass-card" style="text-align:center;">
<div style="font-size:0.7rem; color:#8d9e8f !important; text-transform:uppercase;">Max Price</div>
<div style="font-size:1.2rem; font-weight:600; color:#66bb6a !important;">₹{local_market.get('max_price_quintal',0)}</div>
<div style="font-size:0.65rem; color:#6b7c6d !important;">per quintal</div>
</div>""", unsafe_allow_html=True)
                    
                    st.markdown(f"""<div style="text-align:center; margin:0.5rem 0;">
<span class="metric-pill" style="font-size:0.9rem; padding:8px 20px; background:rgba(46,125,50,0.2); border:1px solid rgba(76,175,80,0.3); border-left:none;">
💰 Total Revenue for {input_data.get('yield_amount', 2500)} kg = <strong>₹{local_market['total_revenue']:,.0f}</strong>
</span>
</div>""", unsafe_allow_html=True)

                # ─── Nearby Markets Comparison ────────────────────────────
                    st.markdown('<div class="section-header">Nearby Markets</div>', unsafe_allow_html=True)

                    # Find the max price for bar chart scaling
                    max_price = max(m["price_per_kg"] for m in nearby_markets) if nearby_markets else 1
                    local_price = local_market["price_per_kg"] if local_market else 0
                    
                    # Market cards in a 2-column grid
                    for row_start in range(0, len(nearby_markets), 2):
                        cols = st.columns(2)
                        for col_idx in range(2):
                            m_idx = row_start + col_idx
                            if m_idx >= len(nearby_markets):
                                break
                            m = nearby_markets[m_idx]
                            
                            # Safe name extraction
                            disp_name = m.get("market") or m.get("market_name") or "Unknown Mandi"
                            
                            is_best = (best_market_info and 
                                      disp_name == best_market_info.get("market") and 
                                      m.get("district") == best_market_info.get("district"))
                            
                            card_class = "market-card best-market" if is_best else "market-card"
                            best_badge_html = '<div class="best-badge">🏆 BEST</div>' if is_best else ''
                            
                            profit = m.get("profit_vs_local", 0)
                            profit_class = "profit-up" if profit > 0 else "profit-down"
                            profit_sign = "+" if profit > 0 else ""
                            profit_icon = "📈" if profit > 0 else "📉"
                            
                            # Price bar width (relative to max)
                            bar_width = min(100, int((m["price_per_kg"] / max_price) * 100)) if max_price > 0 else 50
                            
                            with cols[col_idx]:
                                st.markdown(f"""<div class="{card_class}">
{best_badge_html}
<div class="market-name">{disp_name}</div>
<div class="market-district">📍 {m.get('district', 'N/A')}, {m.get('state', 'N/A')}</div>
<div class="price-tag">₹{m.get('price_per_kg', 0)}<span class="price-unit"> /kg</span></div>
<div class="price-bar-container">
<div class="price-bar market" style="width:{bar_width}%;">₹{m.get('price_per_kg',0)}/kg</div>
</div>
<div style="margin-top:10px;">
<span class="metric-pill distance">📏 {m.get('distance_km',0)} km</span>
<span class="metric-pill time">⏱️ {m.get('drive_hours',0)} hrs</span>
<span class="metric-pill cost">🚚 ₹{m.get('transport_cost', 0):,.0f}</span>
</div>
<div style="margin-top:8px; display:flex; justify-content:space-between; align-items:center;">
<div>
<span style="font-size:0.7rem; color:#8d9e8f !important;">Net after transport:</span><br>
<span style="font-size:1rem; font-weight:700; color:#aed581 !important;">₹{m.get('net_price_per_kg',0)}/kg</span>
</div>
<span class="metric-pill {profit_class}" style="font-weight:700;">{profit_icon} {profit_sign}₹{profit:,.0f}</span>
</div>
</div>""", unsafe_allow_html=True)
                    
                    # Translated Table Section
                    lang_headers = {
                        "Tamil": ["சந்தை", "மாவட்டம்", "மாநிலம்", "விலை (₹/கிலோ)", "தூரம் (கி.மீ)", "பயணம் (மணி)", "போக்குவரத்து (₹)", "நிகர விலை (₹)", "லாபம்"],
                        "Hindi": ["बाज़ार", "ज़िला", "राज्य", "क़ीमत (₹/किलो)", "दूरी (किमी)", "यात्रा (घंटे)", "परिवहन क्षुल्क (₹)", "शुद्ध मूल्य (₹)", "लाभ"],
                        "Malayalam": ["മാർക്കറ്റ്", "ജില്ല", "സംസ്ഥാനം", "വില (₹/Kg)", "ദൂരം (km)", "സമയം (hrs)", "ഗതാഗതം (₹)", "വല വില (₹)", "ലാഭം"],
                        "Telugu": ["మార్కెట్", "జిల్లా", "రాష్ట్రం", "ధర (₹/kg)", "దూరం (కి.మీ)", "ప్రయాణం (గంటలు)", "రవాణా (₹)", "నికర ధర (₹)", "లాభం"]
                    }
                    
                    table_data = []
                    for m in nearby_markets:
                        profit = m.get("profit_vs_local", 0)
                        # Ensure we get a name safely
                        disp_name = m.get("market") or m.get("market_name") or "Unknown Mandi"
                        table_data.append({
                            "Market": disp_name,
                            "District": m.get("district", "N/A"),
                            "State": m.get("state", "N/A"),
                            "Price (₹/kg)": m.get("price_per_kg", 0),
                            "Distance (km)": m.get("distance_km", 0),
                            "Drive (hrs)": m.get("drive_hours", 0),
                            "Transport (₹)": f"₹{m.get('transport_cost', 0):,.0f}",
                            "Net (₹/kg)": m.get("net_price_per_kg", 0),
                            "Profit vs Local": f"{'+' if profit > 0 else ''}₹{profit:,.0f}",
                        })
                    
                    df_markets = pd.DataFrame(table_data)
                    df_translated = df_markets.copy()
                    
                    if st.session_state.target_lang in lang_headers:
                        st.markdown(f'<div class="section-header">📋 {st.session_state.target_lang} Price Comparison Table</div>', unsafe_allow_html=True)
                        df_translated.columns = lang_headers[st.session_state.target_lang]
                    else:
                        st.markdown('<div class="section-header">📋 Complete Price Comparison Table</div>', unsafe_allow_html=True)
                        df_translated.columns = ["Market", "District", "State", "Price (₹/kg)", "Distance (km)", "Drive (hrs)", "Transport (₹)", "Net (₹/kg)", "Profit vs Local"]
                        
                    st.dataframe(df_translated, use_container_width=True, hide_index=True)

                # ─── AI Advisory — Bilingual Display ──────────────────────
                st.markdown('<div class="section-header">🤖 AI Market Advisory</div>', unsafe_allow_html=True)
                
                # Split advisory into regional and English parts
                advisory_parts = advisory_text.split("---")
                
                if len(advisory_parts) >= 2:
                    regional_text = advisory_parts[0].strip()
                    english_text = advisory_parts[1].strip()
                else:
                    regional_text = advisory_text
                    english_text = ""
                
                # Regional language card
                lang_labels = {
                    'Tamil': '🟢 தமிழ் (TAMIL)',
                    'Hindi': '🟢 हिन्दी (HINDI)',
                    'Malayalam': '🟢 മലയാളം (MALAYALAM)',
                    'Telugu': '🟢 తెలుగు (TELUGU)',
                }
                lang_label = lang_labels.get(st.session_state.target_lang, '🟢 REGIONAL')

                st.markdown(f"""
                <div class="advisory-regional">
                    <div class="advisory-label" style="color:#66bb6a !important;">{lang_label}</div>
                    <div class="advisory-text">{regional_text}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # English translation card
                if english_text:
                    st.markdown(f"""
                    <div class="advisory-english">
                        <div class="advisory-label" style="color:#42a5f5 !important;">🔵 ENGLISH TRANSLATION</div>
                        <div class="advisory-text">{english_text}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # ─── Weather Strip ────────────────────────────────────────
                st.markdown('<div class="section-header">🌤️ Live Weather & Environment</div>', unsafe_allow_html=True)
                
                w_cols = st.columns(4)
                with w_cols[0]:
                    st.markdown(f"""
                    <div class="glass-card" style="text-align:center;">
                        <div style="font-size:2rem;">🌡️</div>
                        <div style="font-size:1.3rem; font-weight:700; color:#ffb74d !important;">{climate.get('temperature_celsius', 'N/A')}°C</div>
                        <div style="font-size:0.7rem; color:#8d9e8f !important;">Temperature</div>
                    </div>
                    """, unsafe_allow_html=True)
                with w_cols[1]:
                    st.markdown(f"""
                    <div class="glass-card" style="text-align:center;">
                        <div style="font-size:2rem;">💧</div>
                        <div style="font-size:1.3rem; font-weight:700; color:#42a5f5 !important;">{climate.get('relative_humidity_percent', 'N/A')}%</div>
                        <div style="font-size:0.7rem; color:#8d9e8f !important;">Humidity</div>
                    </div>
                    """, unsafe_allow_html=True)
                with w_cols[2]:
                    st.markdown(f"""
                    <div class="glass-card" style="text-align:center;">
                        <div style="font-size:2rem;">🌧️</div>
                        <div style="font-size:1.3rem; font-weight:700; color:#64b5f6 !important;">{climate.get('precipitation_mm', 'N/A')} mm</div>
                        <div style="font-size:0.7rem; color:#8d9e8f !important;">Precipitation</div>
                    </div>
                    """, unsafe_allow_html=True)
                with w_cols[3]:
                    aqi = climate.get('current_aqi', 'N/A')
                    aqi_color = "#66bb6a" if isinstance(aqi, (int, float)) and aqi < 50 else "#ffb74d" if isinstance(aqi, (int, float)) and aqi < 100 else "#ef5350"
                    st.markdown(f"""
                    <div class="glass-card" style="text-align:center;">
                        <div style="font-size:2rem;">🌫️</div>
                        <div style="font-size:1.3rem; font-weight:700; color:{aqi_color} !important;">{aqi}</div>
                        <div style="font-size:0.7rem; color:#8d9e8f !important;">Air Quality Index</div>
                    </div>
                    """, unsafe_allow_html=True)

                # ─── Audio Playback ───────────────────────────────────────
                # Generate gTTS for the regional language portion only
                cleaned_advisory = clean_text_for_speech(regional_text)
                lang_codes = {'Hindi': 'hi', 'Tamil': 'ta', 'Malayalam': 'ml', 'Telugu': 'te', 'English': 'en'}
                current_code = lang_codes.get(st.session_state.target_lang, 'en')
                clean_speech = cleaned_advisory.replace('*', '').replace('#', '')
                tts = gTTS(text=clean_speech, lang=current_code, slow=False)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                tts.save(temp_file.name)
                
                time.sleep(1)
                st.audio(temp_file.name, format="audio/mp3", autoplay=True)
                
                # ─── Data Source Footer ───────────────────────────────────
                st.markdown(f"""
                <div class="data-source">
                    📡 Market prices sourced from <strong>Government of India — data.gov.in (Agmarknet)</strong> | 
                    🗺️ Distance via <strong>OSRM</strong> | 
                    🌤️ Weather via <strong>Open-Meteo</strong> |
                    Last updated: {nearby_markets[0].get('arrival_date', 'Today') if nearby_markets else 'Today'}
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.error(f"Backend Error: {api_response.status_code} - {api_response.text}")

    except sr.UnknownValueError:
        st.error("Speech Recognition could not understand the audio.")
    except json.JSONDecodeError:
        st.error("Failed to parse the data extraction AI's response as valid JSON.")
    except Exception as e:
        st.error(f"Error processing your request: {e}")
