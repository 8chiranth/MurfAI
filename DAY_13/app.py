import streamlit as st
import google.generativeai as genai
import os
import speech_recognition as sr
import pyttsx3
import threading
from dotenv import load_dotenv

# ------------------- Load API Key -------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = "gemini-1.5-flash-latest"

st.title("🎤 AI Voice Agent ")

# ------------------- Session State Init -------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # [(speaker, text), ...]
if "recording" not in st.session_state:
    st.session_state.recording = False  # For Start/Stop toggle

FALLBACK_RESPONSE = "I'm having trouble connecting right now."

# ------------------- Helper: TTS Playback (Threaded) ------------
def tts_speak_thread(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def tts_playback(text):
    try:
        t = threading.Thread(target=tts_speak_thread, args=(text,))
        t.start()
    except Exception:
        st.warning("⚠ Unable to play audio.")

# ------------------- Speech-to-Text -------------------
def stt_listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Listening... Speak now.")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        st.warning("❌ Could not understand your voice.")
    except sr.RequestError as e:
        st.warning(f"⚠ Speech recognition error: {e}")
    return None

# ------------------- CSS Styling for Button -------------------
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 12px 20px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        transition: background-color 0.3s ease, transform 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# ------------------- Start/Stop Button -------------------
if st.button("⏺ Start Recording" if not st.session_state.recording else "⏹ Stop Recording"):
    if not st.session_state.recording:
        st.session_state.recording = True
        user_input = stt_listen()
        
        if user_input:
            st.session_state.chat_history.append(("You", user_input))
            
            # Prepare conversation history
            gemini_history = []
            for speaker, content in st.session_state.chat_history:
                if speaker not in ("System",):
                    role = "user" if speaker == "You" else "model"
                    gemini_history.append({"role": role, "parts": [{"text": content}]})

            # Get LLM response
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                chat = model.start_chat(history=gemini_history[:-1])
                response = chat.send_message(user_input)
                ai_text = response.text.strip()
            except Exception as e:
                st.error(f"LLM Error: {e}")
                ai_text = FALLBACK_RESPONSE

            st.session_state.chat_history.append(("AI", ai_text))
            try:
                tts_playback(ai_text)
            except Exception:
                st.warning("⚠ Unable to play audio. Showing text only.")
        
        st.session_state.recording = False  # Auto-stop after processing
    else:
        st.session_state.recording = False
        st.info("🛑 Recording stopped.")

# ------------------- Display Chat History -------------------
st.markdown("### 💬 Conversation")
for speaker, content in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"🧑 **You:** {content}")
    elif speaker == "AI":
        st.markdown(f"🤖 **AI:** {content}")
    elif speaker == "System":
        st.markdown(f"⚙️ **System:** {content}")
