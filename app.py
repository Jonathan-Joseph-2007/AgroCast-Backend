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

st.set_page_config(page_title="AgroCast Voice Assistant", layout="centered")

@st.cache_resource
def get_openai_client():
    load_dotenv()
    return OpenAI(
        base_url="https://api.featherless.ai/v1",
        api_key=os.getenv('FEATHERLESS_API_KEY', '')
    )

client = get_openai_client()

st.title("AgroCast Voice Assistant")

# Center the single audio recorder widget
if 'target_lang' not in st.session_state:
    st.session_state.target_lang = "Tamil"

st.write("### Select Language")
lang_cols = st.columns(4)
languages = ['Tamil', 'Hindi', 'Malayalam', 'Telugu']
for i, lang in enumerate(languages):
    if lang_cols[i].button(lang, use_container_width=True):
        st.session_state.target_lang = lang

st.info(f"**Selected Language:** {st.session_state.target_lang}")

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
            system_prompt = (
                f"You are a Strict Data Extractor. Analyze the user's voice text and output ONLY a JSON.\n\n"
                f"The user has selected {st.session_state.target_lang}. Translate the extracted data and the final response strictly into this language script.\n\n"
                "Identify the intent:\n"
                "- If the user asks about price, intent = 'price_check'.\n"
                "- If they ask about weather/climate, intent = 'climate_check'.\n"
                "- If they ask about selling/market, intent = 'full_advice'.\n\n"
                "Extract the crop and any numbers mentioned.\n\n"
                "Validation: Ensure the AI always outputs numbers. If a user asks for 'Price' but doesn't mention a crop, look at the previous context or default to 'Tomato'. If it can't find a number in the speech, it must use these defaults: "
                "yield_amount: 2500, current_price: 40, distant_market_price: 55, transport_cost: 15000.\n\n"
                "Output JSON keys: intent, language, crop, yield_amount, current_price, distant_market_price, transport_cost."
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
            
            # Add required coordinates
            payload["lat"] = 11.0168
            payload["lon"] = 76.9558
            
            # Send payload to backend
            API_URL = "https://agrocast-backend.onrender.com/predict"
            api_response = requests.post(API_URL, json=payload)
            
            if api_response.status_code == 200:
                data = api_response.json()
                
                # Display output
                advisory_text = data.get("advisory", "No advice generated.")
                st.success(advisory_text)
                
                with st.expander("Technical Logs (Model Verification)"):
                    st.write("**Payload sent to Backend:**")
                    st.json(payload)
                    st.write("**Raw profit_improvement from PKL model:**", data.get("forecasts", {}).get("profit_improvement"))
                
                # Language Mapping for gTTS
                lang_map = {'Hindi': 'hi', 'Tamil': 'ta', 'Telugu': 'te', 'Malayalam': 'ml', 'Kannada': 'kn', 'English': 'en', 'Tanglish': 'ta'}
                extracted_lang = payload.get("language", st.session_state.target_lang)
                lang_code = lang_map.get(extracted_lang, 'en')
                
                # Generate Audio via gTTS
                tts = gTTS(text=advisory_text, lang=lang_code)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                tts.save(temp_file.name)
                
                # Playback
                st.audio(temp_file.name, format="audio/mp3", autoplay=True)
                
            else:
                st.error(f"Backend Error: {api_response.status_code} - {api_response.text}")

    except sr.UnknownValueError:
        st.error("Speech Recognition could not understand the audio.")
    except json.JSONDecodeError:
        st.error("Failed to parse the data extraction AI's response as valid JSON.")
    except Exception as e:
        st.error(f"Error processing your request: {e}")
