import speech_recognition as sr
import logging

logger = logging.getLogger(__name__)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        logger.info("Listening for user input...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        logger.warning("Could not understand voice input.")
        return None
    except sr.RequestError as e:
        logger.error(f"Speech recognition error: {e}")
        return None
