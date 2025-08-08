import os
import requests
import time
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
ASSEMBLY_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Static & Templates setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=JSONResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/transcribe/file")
async def transcribe_file(audio: UploadFile = File(...)):
    try:
        # Step 1: Upload to AssemblyAI
        upload_url = "https://api.assemblyai.com/v2/upload"
        headers = {"authorization": ASSEMBLY_API_KEY}

        upload_res = requests.post(upload_url, headers=headers, data=audio.file)
        if upload_res.status_code != 200:
            return JSONResponse({"success": False, "error": f"Upload failed: {upload_res.text}"})

        audio_url = upload_res.json()["upload_url"]

        # Step 2: Request transcription
        transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
        json_data = {"audio_url": audio_url}
        trans_res = requests.post(transcript_endpoint, headers=headers, json=json_data)

        if trans_res.status_code != 200:
            return JSONResponse({"success": False, "error": f"Transcription request failed: {trans_res.text}"})

        trans_id = trans_res.json()["id"]

        # Step 3: Poll for result
        while True:
            poll_res = requests.get(f"{transcript_endpoint}/{trans_id}", headers=headers).json()
            if poll_res["status"] == "completed":
                return JSONResponse({"success": True, "transcript": poll_res["text"]})
            elif poll_res["status"] == "error":
                return JSONResponse({"success": False, "error": poll_res["error"]})
            time.sleep(3)

    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})
