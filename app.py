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

st.set_page_config(page_title="AgroCast Voice Assistant", layout="centered")

st.markdown("""
<style>
/* Main background: Very dark forest/night soil */
.stApp {
    background-color: #121E14; 
}
/* Global Text Clarity Fix: Force all standard text to high-contrast pale green/white */
p, span, label, div {
    color: #E8F5E9 !important; 
}
/* Button styling: Bright leaf green for high visibility */
.stButton>button {
    background-color: #2E7D32 !important;
    color: #FFFFFF !important;
    font-weight: bold;
    border-radius: 8px;
    border: 1px solid #4CAF50;
    box-shadow: 0 4px 6px rgba(0,0,0,0.4);
}
.stButton>button:hover {
    background-color: #4CAF50 !important;
    color: #121E14 !important; /* Dark text on hover for contrast */
}
/* Headers: Bright pastel green so they pop in the dark */
h1, h2, h3 {
    color: #81C784 !important; 
}
/* Stylized Header overrides */
.custom-header { text-align: center; color: #81C784; }
.custom-subheader { text-align: center; color: #BCAAA4; } /* Light warm brown */
/* Success/Notification boxes for dark mode */
div[data-baseweb="notification"] {
    background-color: #1B5E20 !important; /* Deep green card */
    border-left: 5px solid #81C784; /* Bright green accent line */
}
/* Ensure text inside the success box is pure white */
div[data-baseweb="notification"] p {
    color: #FFFFFF !important;
    font-size: 16px;
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

st.markdown("<h1 class='custom-header'>🌱 AgroCast AI</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='custom-subheader'>Smart Market & Climate Advisory</h4>", unsafe_allow_html=True)

# Center the single audio recorder widget
if 'target_lang' not in st.session_state:
    st.session_state.target_lang = "Tamil"

st.write("### Select Language")
lang_cols = st.columns(4)

# Map native scripts to internal English values
LANGUAGE_UI_MAP = {
    'தமிழ்': 'Tamil',
    'हिन्दी': 'Hindi',
    'മലയാളം': 'Malayalam',
    'తెలుగు': 'Telugu'
}

for i, (native_script, english_name) in enumerate(LANGUAGE_UI_MAP.items()):
    if lang_cols[i].button(native_script, use_container_width=True):
        st.session_state.target_lang = english_name

# Display the selected language using its native script
current_native = next((k for k, v in LANGUAGE_UI_MAP.items() if v == st.session_state.target_lang), st.session_state.target_lang)
st.info(f"**Selected Language:** {current_native}")

st.markdown("---")

col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    st.write("Click the microphone to record your question:")
    audio_bytes = audio_recorder()

if audio_bytes:
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes)
        
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile("temp.wav") as source:
            audio_data = recognizer.record(source)
            user_text = recognizer.recognize_google(audio_data)
            
        st.info(f"**You said:** {user_text}")
        
        with st.spinner('Processing...'):
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
                
            # --- 2. DATA EXTRACTION ---
            system_prompt = (
                f"You are a Strict Data Extractor. Analyze the user's voice text and output ONLY a JSON.\n\n"
                f"You are a strict native agricultural translator. The user has selected {st.session_state.target_lang}.\n"
                f"CRITICAL RULES FOR THE \"advisory\" FIELD:\n"
                f"- It MUST be written 100% in the native {st.session_state.target_lang} script.\n"
                f"- ABSOLUTELY NO English letters (A-Z, a-z) are allowed in the advisory text.\n"
                f"- Translate all technical terms (Profit, Yield, AQI, Weather, Market) into pure {st.session_state.target_lang}.\n"
                f"- Do not use transliterated English (e.g., do not write 'profit' in Malayalam script; use the actual Malayalam word for profit).\n\n"
                "Identify the intent:\n"
                "- If the user asks about price, intent = 'price_check'.\n"
                "- If they ask about weather/climate, intent = 'climate_check'.\n"
                "- If they ask about selling/market, intent = 'full_advice'.\n\n"
                "Extract the crop and any numbers mentioned. If the user mentions a regional name like \"Aalu\", map it to its English equivalent \"Potato\" before sending it to the backend ML models.\n\n"
                "Validation: Ensure the AI always outputs numbers. If a user asks for 'Price' but doesn't mention a crop, look at the previous context or default to 'Tomato'. If it can't find a number in the speech, it must use these defaults: "
                "yield_amount: 2500, current_price: 40, distant_market_price: 55.\n\n"
                "Output JSON keys: intent, language, crop, yield_amount, current_price, distant_market_price."
            )
            
            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3-0324",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ]
            )
            
            # Parse the JSON response, removing backticks if deepseek added them
            extraction_str = response.choices[0].message.content.strip()
            if extraction_str.startswith("```json"):
                extraction_str = extraction_str[7:-3].strip()
            elif extraction_str.startswith("```"):
                extraction_str = extraction_str[3:-3].strip()
                
            payload = json.loads(extraction_str)
            
            # --- 3. BACKEND API CALL ---
            API_URL = "https://agrocast-backend.onrender.com/predict"
            time.sleep(2.5)  # Wait for the Featherless AI concurrency limit to safely clear
            api_response = requests.post(API_URL, json=payload)
            
            if api_response.status_code == 200:
                data = api_response.json()
                
                # Display output
                advisory_text = data.get("advisory", "No advice generated.")
                st.success(advisory_text)
                
            # with st.expander("Technical Logs (Model Verification)"):
            #     st.write("**Payload sent to Backend:**")
            #     st.json(payload)
            #     st.write("**Raw profit_improvement from PKL model:**", data.get("forecasts", {}).get("profit_improvement"))
                
                # Generate Audio via gTTS
                cleaned_advisory = clean_text_for_speech(advisory_text)
                lang_codes = {'Hindi': 'hi', 'Tamil': 'ta', 'Malayalam': 'ml', 'Telugu': 'te', 'English': 'en'}
                current_code = lang_codes.get(st.session_state.target_lang, 'en')
                clean_text = cleaned_advisory.replace('*', '').replace('#', '')
                tts = gTTS(text=clean_text, lang=current_code, slow=False)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                tts.save(temp_file.name)
                
                # Playback
                time.sleep(1)
                st.audio(temp_file.name, format="audio/mp3", autoplay=True)
                
            else:
                st.error(f"Backend Error: {api_response.status_code} - {api_response.text}")

    except sr.UnknownValueError:
        st.error("Speech Recognition could not understand the audio.")
    except json.JSONDecodeError:
        st.error("Failed to parse the data extraction AI's response as valid JSON.")
    except Exception as e:
        st.error(f"Error processing your request: {e}")
