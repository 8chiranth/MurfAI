import pyttsx3
import logging
import threading

logger = logging.getLogger(__name__)

def speak(text: str):
    def run():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    try:
        thread = threading.Thread(target=run)
        thread.start()
    except Exception as e:
        logger.error(f"TTS Error: {e}")
