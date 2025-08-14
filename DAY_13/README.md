# 🎤 AI Voice Agent

Welcome to the **AI Voice Agent** project!  
This is an interactive voice chatbot powered by Google's Gemini LLM, built using Python and Streamlit. Users can converse with the AI by speaking directly into their microphones, and receive both text and spoken replies.

---

## Technologies Used

- **Streamlit**: UI framework for interactive web apps.
- **Google Generative AI (Gemini)**: LLM for intelligent responses.
- **SpeechRecognition**: Converts speech input to text.
- **pyttsx3**: Text-to-speech for AI replies.
- **dotenv**: Secure environment variable handling.
- **threading**: Non-blocking audio playback.

---

## Architecture

- **Streamlit Frontend**: Displays UI, captures user actions.
- **Speech-to-Text**: Listens to microphone input, transcribes to text.
- **LLM (Gemini API)**: Processes chat history, generates responses.
- **Text-to-Speech**: AI replies are played aloud using pyttsx3.
- **Session Management**: Maintains conversation history.


---

## Features

- **Voice Conversation**: Talk directly with AI.
- **Text-to-Speech Playback**: AI replies are audible.
- **Rich Chat History**: Scrollable, toggle for each speaker.
- **Gemini Integration**: State-of-the-art contextual LLM.
- **One-click Recording**: Start/Stop button with custom style.
- **Error Handling**: Informative feedback on API and audio errors.

---

## Setup & Instructions

1. **Clone the Repository**


2. **Install Requirements**


3. **Set Up Environment Variables**

Create a `.env` file in the root directory:


> **Note:** You must have access to the Gemini API; get your key from Google AI Studio.

4. **Run the Application**


5. **Using the App**

- Click **Start Recording** to begin.
- Speak into your microphone.
- Wait for AI reply (voice + text).
- Stop Recording anytime.

---

## Environment Variables

| Variable       | Description               | Example Value              |
|----------------|---------------------------|----------------------------|
| GOOGLE_API_KEY | Gemini API key (required) | ya29.A0ARrdaM...           |

---

## Screenshots

### Main UI
*(Add your screenshot here)*

---

## API Server

*No separate API server required!*  
All logic runs locally via Streamlit.  
Gemini API calls are made directly from Python.

---

## Customizing

- Add more features (e.g. support for other LLMs, better UI, hotword listening).
- Try new buttons, themes, or avatar icons.
- Tweak error messages and feedback.

---

> 🌟 **Personalize this README!** Replace links, add your name, and upload your own UI screenshots to stand out on LinkedIn.
