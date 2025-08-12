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

st.title("🎤 AI Voice Agent (Day 11 - With Error Handling)")

# ------------------- Session State Init -------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # [(speaker, text), ...]

# Optional: simulate failures
simulate_stt_error = st.checkbox("Simulate STT Error")
simulate_llm_error = st.checkbox("Simulate LLM Error")
simulate_tts_error = st.checkbox("Simulate TTS Error")

FALLBACK_RESPONSE = "I'm having trouble connecting right now."

# ------------------- Speech-to-Text -------------------
def stt_listen():
    if simulate_stt_error:
        raise Exception("Simulated STT failure.")
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

# ------------------- pyttsx3 Text-to-Speech in Thread -------------------
def tts_speak_thread(text):
    if simulate_tts_error:
        raise Exception("Simulated TTS failure.")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def tts_playback(text):
    try:
        t = threading.Thread(target=tts_speak_thread, args=(text,))
        t.start()
    except Exception as e:
        st.error(f"TTS Error: {e}")
        st.warning("⚠ Using fallback TTS.")
        # We can choose to skip audio here (already showing text on screen)

# ------------------- Main Interaction -------------------
if st.button("🎤 Speak"):
    try:
        user_input = stt_listen()
    except Exception as e:
        st.error(f"STT Error: {e}")
        user_input = None

    if user_input:
        st.session_state.chat_history.append(("You", user_input))

        # Prepare conversation history
        gemini_history = []
        for speaker, content in st.session_state.chat_history:
            role = "user" if speaker == "You" else "model"
            gemini_history.append({"role": role, "parts": [{"text": content}]})

        # Get LLM response
        try:
            if simulate_llm_error:
                raise Exception("Simulated LLM failure.")

            model = genai.GenerativeModel(MODEL_NAME)
            chat = model.start_chat(history=gemini_history[:-1])  
            response = chat.send_message(user_input)
            ai_text = response.text.strip()
        except Exception as e:
            st.error(f"LLM Error: {e}")
            ai_text = FALLBACK_RESPONSE

        # Save AI reply
        st.session_state.chat_history.append(("AI", ai_text))

        # Speak AI reply
        try:
            tts_playback(ai_text)
        except Exception as e:
            st.error(f"TTS Error: {e}")
            st.warning("⚠ Unable to play audio. Showing text only.")

# ------------------- Display Chat History -------------------
st.markdown("### 💬 Conversation")
for speaker, content in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"🧑 **You:** {content}")
    else:
        st.markdown(f"🤖 **AI:** {content}")
