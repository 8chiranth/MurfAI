from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os
import assemblyai as aai
from werkzeug.utils import secure_filename
from datetime import datetime

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

aai_api_key = os.getenv("ASSEMBLYAI_API_KEY")
if not aai_api_key:
    raise RuntimeError("ASSEMBLYAI_API_KEY not set in environment.")

aai.settings.api_key = aai_api_key

app = Flask(__name__, static_folder='static', template_folder='templates')

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'webm', 'wav', 'mp3', 'ogg', 'm4a'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health')
def health():
    return jsonify({"status": "ok", "message": "Server is healthy."})

@app.route('/tts/test')
def tts_test():
    return jsonify({"success": True, "message": "TTS test successful."})

# Example TTS endpoint (dummy; replace with your Murf-based one)
@app.route('/tts', methods=['POST'])
def fake_tts():
    data = request.get_json()
    text = data.get("text", "")
    fake_audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    return jsonify({
        "success": True,
        "audio_url": fake_audio_url,
        "voice_used": data.get("voice_id", "en-US-ken"),
        "format": data.get("format", "mp3"),
        "characters_used": len(text)
    })

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'success': False, 'error': 'No audio file part'}), 400
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected audio file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        file_size = os.path.getsize(save_path)
        return jsonify({
            'success': True,
            'filename': filename,
            'content_type': file.content_type,
            'size': file_size
        })
    return jsonify({'success': False, 'error': 'Invalid file type'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/transcribe/file', methods=['POST'])
def transcribe_file():
    if 'audio' not in request.files:
        return jsonify({'success': False, 'error': 'No audio file provided.'}), 400
    file = request.files['audio']
    audio_bytes = file.read()
    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_bytes)
        return jsonify({'success': True, 'transcript': transcript.text}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/')
def index():
    # If you have templates/index.html, use render_template('index.html')
    # If not, serve single-file HTML (see next section)
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == "__main__":
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host=host, port=port, debug=debug)
