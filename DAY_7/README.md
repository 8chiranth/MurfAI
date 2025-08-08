# 🎤 Echo Bot with Murf TTS + AssemblyAI STT

A Flask web app that:
1. Records your voice in the browser.
2. Sends it to **AssemblyAI** for transcription.
3. Sends the transcript to **Murf's Text-to-Speech** API.
4. Plays back the Murf-generated voice in the browser.

## 🚀 Features
- Neon-themed frontend (HTML/CSS).
- Two modes:
  - **TTS Generator** → Type text & get Murf audio.
  - **Echo Bot** → Speak, transcribe, then echo in Murf's voice.
- Backend integration with Murf & AssemblyAI APIs.

---

## 📦 Installation

```bash
git clone https://github.com/your-username/echo-bot.git
cd echo-bot
pip install -r requirements.txt
