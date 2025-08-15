import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

from schemas import Message
from services.stt import listen
from services.tts import speak

# --------- Logging Setup ---------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

# --------- Load API Key from .env ---------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "gemini-1.5-flash-latest"

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in .env file.")
    logger.critical("API Key missing. Stopping app.")
    st.stop()

# --------- Configure Gemini API ---------
genai.configure(api_key=GOOGLE_API_KEY)

st.title("🎤 AI Voice Agent")

# --------- Session State ---------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # List[Message]
if "recording" not in st.session_state:
    st.session_state.recording = False  # For Start/Stop toggle

FALLBACK_RESPONSE = "I'm having trouble connecting right now."

# --------- CSS for Button ---------
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

# --------- Main Button Logic ---------
if st.button("⏺ Start Recording" if not st.session_state.recording else "⏹ Stop Recording"):
    if not st.session_state.recording:
        st.session_state.recording = True
        user_input = listen()
        logger.info(f"User input: {user_input}")

        if user_input:
            st.session_state.chat_history.append(Message(role="user", text=user_input))

            # --------- Map roles for Gemini API ---------
            gemini_history = []
            for m in st.session_state.chat_history:
                # Map 'user' -> 'user', 'ai' -> 'model'
                role = "user" if m.role == "user" else "model"
                gemini_history.append({"role": role, "parts": [{"text": m.text}]})

            # --------- Get LLM response ---------
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                chat = model.start_chat(history=gemini_history[:-1])  # exclude the latest user input
                response = chat.send_message(user_input)
                ai_text = response.text.strip()
                logger.info(f"AI response: {ai_text}")
            except Exception as e:
                st.error(f"LLM Error: {e}")
                logger.error(f"LLM Error: {e}")
                ai_text = FALLBACK_RESPONSE

            st.session_state.chat_history.append(Message(role="ai", text=ai_text))
            speak(ai_text)
        else:
            st.warning("❌ Could not understand your voice.")

        st.session_state.recording = False  # Auto-stop after processing
    else:
        st.session_state.recording = False
        st.info("🛑 Recording stopped.")
        logger.info("Recording stopped by user.")

# --------- Display Chat History ---------
st.markdown("### 💬 Conversation")
for msg in st.session_state.chat_history:
    if msg.role == "user":
        st.markdown(f"🧑 **You:** {msg.text}")
    elif msg.role == "ai":
        st.markdown(f"🤖 **AI:** {msg.text}")
