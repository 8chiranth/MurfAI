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

st.title("🎤 AI Voice Agent")

# ------------------- Session State Init -------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # [(speaker, text), ...]

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

# ------------------- pyttsx3 Text-to-Speech in Thread -------------------
def tts_speak_thread(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def tts_playback(text):
    t = threading.Thread(target=tts_speak_thread, args=(text,))
    t.start()

# ------------------- Main Interaction -------------------
if st.button("🎤 Speak"):
    user_input = stt_listen()
    if user_input:
        # Save user's message
        st.session_state.chat_history.append(("You", user_input))

        # Prepare full conversation history for Gemini
        gemini_history = []
        for speaker, content in st.session_state.chat_history:
            role = "user" if speaker == "You" else "model"
            gemini_history.append({"role": role, "parts": [{"text": content}]})

        # Send it to Gemini
        model = genai.GenerativeModel(MODEL_NAME)
        chat = model.start_chat(history=gemini_history[:-1])  # exclude the new user input (will send separately)
        response = chat.send_message(user_input)
        ai_text = response.text.strip()

        # Save AI's reply
        st.session_state.chat_history.append(("AI", ai_text))

        # Speak AI's reply
        tts_playback(ai_text)

# ------------------- Display Chat History -------------------
for speaker, content in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"🧑 You:** {content}")
    else:
        st.markdown(f"🤖 AI:** {content}")