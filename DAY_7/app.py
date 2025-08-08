import os
import time
import requests
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables (.env file)
load_dotenv()
ASSEMBLY_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")

# Ensure you're running from the folder that contains 'static/' and 'templates/'
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Models
class EchoResponse(BaseModel):
    audio_url: str
    transcription: str
    message: str

# AssemblyAI transcription helper
def transcribe_audio_assemblyai(audio_data: bytes, api_key: str):
    upload_url = "https://api.assemblyai.com/v2/upload"
    headers = {"authorization": api_key}
    upload_res = requests.post(upload_url, headers=headers, data=audio_data)
    if upload_res.status_code != 200:
        raise Exception(f"Upload failed: {upload_res.text}")
    audio_url = upload_res.json()["upload_url"]

    transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
    trans_res = requests.post(transcript_endpoint, headers=headers, json={"audio_url": audio_url})
    if trans_res.status_code != 200:
        raise Exception(f"Transcription request failed: {trans_res.text}")
    trans_id = trans_res.json()["id"]

    while True:
        poll_res = requests.get(f"{transcript_endpoint}/{trans_id}", headers=headers).json()
        if poll_res["status"] == "completed":
            return poll_res["text"]
        elif poll_res["status"] == "error":
            raise Exception(f"Transcription error: {poll_res.get('error', 'Unknown error')}")
        time.sleep(3)

class Transcriber:
    def __init__(self, api_key):
        self.api_key = api_key
    def transcribe(self, audio_data):
        try:
            text = transcribe_audio_assemblyai(audio_data, self.api_key)
            class Result:
                def __init__(self, text):
                    self.text = text
                    self.error = None
            return Result(text)
        except Exception as e:
            class Result:
                def __init__(self, error):
                    self.text = None
                    self.error = str(error)
            return Result(str(e))
transcriber = Transcriber(ASSEMBLY_API_KEY)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/tts")
async def tts(req: dict):
    """
    Body: { "text": str, "voice_id": str, "format": str }
    Returns: { "audio_url": str }
    """
    # Dummy: Replace with your real TTS API integration as needed.
    # This just returns a sample file.
    return JSONResponse({"audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"})

@app.post("/tts/echo", response_model=EchoResponse)
async def tts_echo(file: UploadFile = File(...)):
    if not MURF_API_KEY or not ASSEMBLY_API_KEY:
        raise HTTPException(500, "API keys not configured")
    allowed_types = [
        "audio/webm", "audio/wav", "audio/mp3", "audio/mpeg", "audio/ogg", "audio/m4a"
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(400, f"Invalid file type. Allowed: {allowed_types}")

    audio_data = await file.read()
    if not audio_data:
        raise HTTPException(400, "Empty audio file")

    transcript = transcriber.transcribe(audio_data)
    if transcript.error:
        raise HTTPException(500, f"Transcription failed: {transcript.error}")

    transcribed_text = transcript.text or "[No speech detected]"

    if not transcript.text or transcript.text.strip() == "":
        return EchoResponse(audio_url="", transcription="[No speech detected]", message="No speech detected in audio")

    murf_url = "https://api.murf.ai/v1/speech/generate"
    headers = {
        "api-key": MURF_API_KEY,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    payload = {
        "voiceId": "en-US-natalie",
        "style": "Conversational",
        "text": transcribed_text,
        "format": "MP3",
        "sampleRate": 44100,
        "effect": "none",
    }
    try:
        murf_response = requests.post(murf_url, headers=headers, json=payload, timeout=60)
    except Exception as e:
        raise HTTPException(500, f"Murf API request failed: {str(e)}")
    if murf_response.status_code != 200:
        raise HTTPException(murf_response.status_code, f"Murf TTS failed: {murf_response.text}")
    murf_data = murf_response.json()
    audio_url = murf_data.get("audioFile", "")
    if not audio_url:
        raise HTTPException(500, "No audioFile URL in Murf response")

    return EchoResponse(
        audio_url=audio_url,
        transcription=transcribed_text,
        message="Echo generated successfully with Murf voice!"
    )

@app.post("/transcribe/file")
async def transcribe_file(audio: UploadFile = File(...)):
    """
    Uploads audio to AssemblyAI and returns transcription.
    """
    try:
        audio_data = await audio.read()
        text = transcribe_audio_assemblyai(audio_data, ASSEMBLY_API_KEY)
        return JSONResponse({"success": True, "transcript": text})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})
