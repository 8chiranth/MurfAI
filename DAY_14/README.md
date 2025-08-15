🎤 AI Voice Agent
Overview
An interactive, AI-powered voice chatbot built with Streamlit and Google Gemini. The app allows you to speak to your computer, transcribes your voice, responds with intelligent answers, and then speaks those answers back to you. Perfect for hands-free conversations with AI!



Features
Conversational AI powered by Google Gemini

Speech-to-text input via microphone

Text-to-speech output (voice playback)

Chat history display between you and the AI

Easy-to-use web interface

Technologies Used
Python 3.8+

Streamlit

Google Generative AI (Gemini)

SpeechRecognition

pyttsx3

Pydantic

python-dotenv

Logging module

Architecture
Service logic modularized in /services:

services/stt.py: Speech-to-text functionality

services/tts.py: Text-to-speech functionality

API request and response schemas defined in schemas.py

Application state handled with Streamlit's session_state

Logging for error reporting and debugging

Environment variables managed securely via .env files

