# # app.py
# # Import necessary modules from Flask
# from flask import Flask, render_template, request, jsonify
# import requests
# import os
# from datetime import datetime
# import time

# # Try to load environment variables from .env file
# try:
#     from dotenv import load_dotenv
#     load_dotenv()
#     print("✅ Environment variables loaded from .env file")
# except ImportError:
#     print("⚠️  python-dotenv not installed. Using system environment variables only.")

# # Initialize the Flask application
# app = Flask(__name__, static_folder='static', template_folder='templates')

# # Murf API configuration
# MURF_API_URL = os.getenv('MURF_API_URL', 'https://api.murf.ai/v1/speech/generate')
# MURF_AUTH_URL = 'https://api.murf.ai/v1/auth/token'
# MURF_API_KEY = os.getenv('MURF_API_KEY')

# # Cache for auth token (simple in-memory cache)
# auth_token_cache = {
#     'token': None,
#     'expires_at': 0
# }

# # Validate API key
# if not MURF_API_KEY:
#     print("⚠️  WARNING: MURF_API_KEY not found in environment variables!")
#     print("Please set your API key in the .env file or as an environment variable")
# else:
#     print("🔑 Murf API key configured successfully")

# # Define a route for the root URL ('/')
# @app.route('/')
# def index():
#     """
#     This function handles requests to the root URL.
#     It renders and returns the 'index.html' template.
#     """
#     return render_template('index.html')

# def get_murf_auth_token():
#     """
#     Get a valid Murf auth token, generating a new one if needed
#     """
#     current_time = int(time.time() * 1000)  # Current time in milliseconds
    
#     # Check if we have a valid cached token
#     if (auth_token_cache['token'] and 
#         auth_token_cache['expires_at'] > current_time + 60000):  # 1 minute buffer
#         return auth_token_cache['token']
    
#     # Generate a new token
#     try:
#         headers = {
#             'api-key': MURF_API_KEY,
#             'Content-Type': 'application/json'
#         }
        
#         print("🔑 Generating new Murf auth token...")
#         response = requests.post(MURF_AUTH_URL, headers=headers, timeout=10)
        
#         if response.status_code == 200:
#             token_data = response.json()
#             auth_token_cache['token'] = token_data.get('token')
#             auth_token_cache['expires_at'] = token_data.get('expiryInEpochMillis', 0)
            
#             print("✅ Auth token generated successfully")
#             return auth_token_cache['token']
#         else:
#             print(f"❌ Failed to generate auth token: {response.status_code} - {response.text}")
#             return None
            
#     except Exception as e:
#         print(f"❌ Error generating auth token: {str(e)}")
#         return None

# @app.route('/tts/voices', methods=['GET'])
# def get_voices():
#     """
#     Get available voices from Murf API
#     """
#     if not MURF_API_KEY:
#         return jsonify({
#             'error': 'API key not configured',
#             'success': False
#         }), 500
    
#     try:
#         headers = {
#             'api-key': MURF_API_KEY,
#             'Accept': 'application/json'
#         }
        
#         response = requests.get(
#             'https://api.murf.ai/v1/speech/voices',
#             headers=headers,
#             timeout=10
#         )
        
#         if response.status_code == 200:
#             voices_data = response.json()
#             return jsonify({
#                 'success': True,
#                 'voices': voices_data,
#                 'count': len(voices_data) if isinstance(voices_data, list) else 'unknown'
#             })
#         else:
#             return jsonify({
#                 'success': False,
#                 'error': f'Failed to fetch voices: {response.status_code}',
#                 'details': response.text
#             }), response.status_code
            
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': f'Error fetching voices: {str(e)}'
#         }), 500

# @app.route('/tts/key-test', methods=['GET'])
# def test_api_key():
#     """
#     Test if the API key format is correct
#     """
#     if not MURF_API_KEY:
#         return jsonify({
#             'error': 'API key not configured',
#             'success': False
#         })
    
#     return jsonify({
#         'success': True,
#         'api_key_format': 'Valid format' if MURF_API_KEY.startswith('ap2_') else 'Check format - should start with ap2_',
#         'api_key_length': len(MURF_API_KEY),
#         'api_key_preview': f"{MURF_API_KEY[:8]}...{MURF_API_KEY[-8:]}",
#         'message': 'API key configuration looks good'
#     })

# @app.route('/tts/auth-test', methods=['GET'])
# def test_auth():
#     """
#     Test Murf API authentication
#     """
#     if not MURF_API_KEY:
#         return jsonify({
#             'error': 'Murf API key not configured',
#             'success': False
#         }), 500
    
#     auth_token = get_murf_auth_token()
    
#     if auth_token:
#         return jsonify({
#             'success': True,
#             'message': 'Authentication successful',
#             'token_preview': f"{auth_token[:10]}...{auth_token[-10:]}",
#             'expires_at': auth_token_cache['expires_at']
#         })
#     else:
#         return jsonify({
#             'success': False,
#             'error': 'Failed to authenticate with Murf API'
#         }), 401

# @app.route('/tts/test', methods=['GET'])
# def test_tts_endpoint():
#     """
#     Test endpoint to verify TTS functionality is working.
#     """
#     return jsonify({
#         'message': 'TTS endpoint is active',
#         'status': 'success',
#         'endpoint': '/tts',
#         'method': 'POST',
#         'required_fields': ['text'],
#         'optional_fields': ['voice_id', 'format', 'speech_rate', 'pitch'],
#         'api_key_configured': bool(MURF_API_KEY),
#         'example_request': {
#             'text': 'Hello, this is a test message for text to speech conversion.',
#             'voice_id': 'en-US-ken',  # Valid voice ID
#             'format': 'mp3',
#             'speech_rate': 0  # Speech rate: -50 (slow) to 50 (fast), 0 = normal
#         },
#         'common_voice_ids': [
#             'en-US-ken',
#             'en-US-sarah',
#             'en-US-laura',
#             'en-US-wayne',
#             'en-GB-daniel',
#             'en-AU-nicole'
#         ],
#         'test_urls': {
#             'test_endpoint': '/tts/test',
#             'auth_test_endpoint': '/tts/auth-test',
#             'voices_endpoint': '/tts/voices',
#             'main_endpoint': '/tts'
#         }
#     })

# @app.route('/tts', methods=['POST'])
# def text_to_speech():
#     """
#     REST TTS endpoint that accepts text and returns audio URL.
#     Calls Murf's REST TTS API and returns the generated audio file URL.
#     """
#     try:
#         # Check if API key is configured
#         if not MURF_API_KEY:
#             return jsonify({
#                 'error': 'Murf API key not configured. Please set MURF_API_KEY environment variable.',
#                 'success': False
#             }), 500
        
#         # Get JSON data from request
#         data = request.get_json()
        
#         # Validate input
#         if not data or 'text' not in data:
#             return jsonify({
#                 'error': 'Missing required field: text',
#                 'success': False,
#                 'expected_format': {
#                     'text': 'Your text to convert to speech',
#                     'voice_id': 'en-US-ken (optional)',
#                     'format': 'mp3 (optional)',
#                     'speech_rate': '0 (optional, -50 to 50)'
#                 }
#             }), 400
        
#         text_input = data['text']
        
#         if not text_input.strip():
#             return jsonify({
#                 'error': 'Text cannot be empty',
#                 'success': False
#             }), 400
        
#         # Try direct API key authentication first (simpler approach)
#         headers = {
#             'api-key': MURF_API_KEY,
#             'Content-Type': 'application/json',
#             'Accept': 'application/json'
#         }
        
#         # Use a valid voice ID - changed from en-US-davis to en-US-ken
#         voice_id = data.get('voice_id', 'en-US-ken')
        
#         # Murf API payload (adjust parameters as needed)
#         murf_payload = {
#             'text': text_input,
#             'voiceId': voice_id,
#             'audioFormat': data.get('format', 'MP3').upper(),
#             'modelVersion': 'GEN2',  # Use Gen2 for better quality
#             'rate': data.get('speech_rate', 0),  # Speech rate: -50 to 50 (0 = normal speed)
#             'channelType': 'STEREO'
#         }
        
#         print(f"🎤 Making TTS request for text: '{text_input[:50]}...'")
#         print(f"🔑 Using API key: {MURF_API_KEY[:10]}...{MURF_API_KEY[-4:]}")
#         print(f"🎙️ Using voice ID: {voice_id}")
        
#         # Make request to Murf API
#         response = requests.post(
#             MURF_API_URL,
#             headers=headers,
#             json=murf_payload,
#             timeout=30
#         )
        
#         print(f"📡 Murf API response status: {response.status_code}")
#         print(f"📝 Response headers: {dict(response.headers)}")
        
#         # Handle Murf API response
#         if response.status_code == 200:
#             murf_data = response.json()
#             print(f"✅ Success response: {murf_data}")
            
#             # Extract audio URL from Murf response
#             audio_url = murf_data.get('audioFile') or murf_data.get('audio_url') or murf_data.get('url')
            
#             if audio_url:
#                 return jsonify({
#                     'success': True,
#                     'audio_url': audio_url,
#                     'text_processed': text_input,
#                     'voice_used': murf_payload['voiceId'],
#                     'format': murf_payload['audioFormat'],
#                     'timestamp': datetime.now().isoformat(),
#                     'characters_used': murf_data.get('charactersUsed', 0),
#                     'murf_response': murf_data  # Include full response for debugging
#                 }), 200
#             else:
#                 return jsonify({
#                     'error': 'Audio URL not found in Murf response',
#                     'success': False,
#                     'murf_response': murf_data
#                 }), 500
        
#         else:
#             error_details = response.text
#             try:
#                 error_json = response.json()
#                 error_details = error_json
#                 print(f"❌ Error response: {error_json}")
#             except:
#                 print(f"❌ Raw error response: {error_details}")
                
#             return jsonify({
#                 'error': f'Murf API error: {response.status_code}',
#                 'success': False,
#                 'details': error_details,
#                 'status_code': response.status_code,
#                 'request_payload': murf_payload,  # Help debug the request
#                 'suggestion': 'Try using a valid voice ID like: en-US-ken, en-US-sarah, en-US-laura, en-US-wayne'
#             }), response.status_code
            
#     except requests.RequestException as e:
#         print(f"❌ Network error: {str(e)}")
#         return jsonify({
#             'error': f'Network error calling Murf API: {str(e)}',
#             'success': False
#         }), 500
        
#     except Exception as e:
#         print(f"❌ Server error: {str(e)}")
#         return jsonify({
#             'error': f'Server error: {str(e)}',
#             'success': False
#         }), 500

# # Health check endpoint
# @app.route('/health', methods=['GET'])
# def health_check():
#     """
#     Health check endpoint
#     """
#     return jsonify({
#         'status': 'healthy',
#         'timestamp': datetime.now().isoformat(),
#         'endpoints': {
#             'root': '/',
#             'tts': '/tts',
#             'tts_test': '/tts/test',
#             'voices': '/tts/voices',
#             'health': '/health',
#             'docs': '/docs'
#         }
#     })

# # Documentation endpoint (Flask equivalent of FastAPI's /docs)
# @app.route('/docs', methods=['GET'])
# def api_documentation():
#     """
#     API Documentation endpoint - Flask equivalent of FastAPI's /docs
#     """
#     port = int(os.getenv('FLASK_PORT', 5001))
    
#     docs = {
#         'title': 'Flask TTS API Documentation',
#         'description': 'REST API for Text-to-Speech conversion using Murf API',
#         'version': '1.0.0',
#         'base_url': f'http://localhost:{port}',
#         'endpoints': {
#             'GET /': {
#                 'description': 'Home page - renders HTML template',
#                 'response': 'HTML page'
#             },
#             'GET /docs': {
#                 'description': 'API documentation (this page)',
#                 'response': 'JSON documentation'
#             },
#             'GET /health': {
#                 'description': 'Health check endpoint',
#                 'response': {
#                     'status': 'healthy',
#                     'timestamp': 'ISO timestamp',
#                     'endpoints': 'Available endpoints list'
#                 }
#             },
#             'GET /tts/voices': {
#                 'description': 'Get list of available voices from Murf API',
#                 'response': {
#                     'success': True,
#                     'voices': 'Array of voice objects',
#                     'count': 'Number of voices available'
#                 }
#             },
#             'GET /tts/test': {
#                 'description': 'Test endpoint to verify TTS functionality',
#                 'response': {
#                     'message': 'TTS endpoint is active',
#                     'status': 'success',
#                     'common_voice_ids': 'List of valid voice IDs'
#                 }
#             },
#             'POST /tts': {
#                 'description': 'Convert text to speech using Murf API',
#                 'method': 'POST',
#                 'content_type': 'application/json',
#                 'required_fields': ['text'],
#                 'optional_fields': ['voice_id', 'format', 'speech_rate', 'pitch'],
#                 'request_example': {
#                     'text': 'Hello, this is a test message',
#                     'voice_id': 'en-US-ken',
#                     'format': 'mp3',
#                     'speech_rate': 0
#                 },
#                 'valid_voice_ids': [
#                     'en-US-ken',
#                     'en-US-sarah',
#                     'en-US-laura',
#                     'en-US-wayne',
#                     'en-GB-daniel',
#                     'en-AU-nicole'
#                 ],
#                 'success_response': {
#                     'success': True,
#                     'audio_url': 'https://generated-audio-url.com/file.mp3',
#                     'text_processed': 'Your input text',
#                     'voice_used': 'en-US-ken',
#                     'format': 'mp3',
#                     'timestamp': 'ISO timestamp'
#                 },
#                 'error_response': {
#                     'success': False,
#                     'error': 'Error description'
#                 }
#             }
#         },
#         'quick_test_commands': {
#             'test_endpoint': f'curl http://localhost:{port}/tts/test',
#             'get_voices': f'curl http://localhost:{port}/tts/voices',
#             'tts_conversion': f'curl -X POST http://localhost:{port}/tts -H "Content-Type: application/json" -d \'{{"text": "Hello world!", "voice_id": "en-US-ken"}}\'',
#             'health_check': f'curl http://localhost:{port}/health'
#         },
#         'postman_setup': {
#             'method': 'POST',
#             'url': f'http://localhost:{port}/tts',
#             'headers': {
#                 'Content-Type': 'application/json'
#             },
#             'body': {
#                 'text': 'Your text to convert to speech',
#                 'voice_id': 'en-US-ken',
#                 'format': 'mp3',
#                 'speech_rate': 0
#             }
#         }
#     }
    
#     return jsonify(docs)

# # This block ensures the server runs only when the script is executed directly
# if __name__ == '__main__':
#     # Get configuration from environment variables
#     host = os.getenv('FLASK_HOST', '0.0.0.0')
#     port = int(os.getenv('FLASK_PORT', 5001))
#     debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
#     print("=" * 50)
#     print("🚀 Flask TTS Server Starting...")
#     print(f"🌐 Host: {host}")
#     print(f"🔌 Port: {port}")
#     print(f"🐛 Debug: {debug}")
#     print(f"🔑 API Key: {'✅ Configured' if MURF_API_KEY else '❌ Missing'}")
#     print("=" * 50)
#     print("📡 Available endpoints:")
#     print(f"   • Home: http://localhost:{port}/")
#     print(f"   • API Docs: http://localhost:{port}/docs")
#     print(f"   • Auth Test: http://localhost:{port}/tts/auth-test")
#     print(f"   • Voices: http://localhost:{port}/tts/voices")
#     print(f"   • TTS Test: http://localhost:{port}/tts/test")
#     print(f"   • TTS API: http://localhost:{port}/tts")
#     print(f"   • Health: http://localhost:{port}/health")
#     print("=" * 50)
    
#     # Run the app with environment configuration
#     app.run(host=host, port=port, debug=debug)

    
# from flask import send_from_directory
# from werkzeug.utils import secure_filename


# UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# ALLOWED_EXTENSIONS = {'webm', 'wav', 'mp3', 'ogg', 'm4a'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# @app.route('/upload-audio', methods=['POST'])
# def upload_audio():
#     if 'audio' not in request.files:
#         return jsonify({'success': False, 'error': 'No audio file part'}), 400
#     file = request.files['audio']
#     if file.filename == '':
#         return jsonify({'success': False, 'error': 'No selected audio file'}), 400
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(save_path)
#         file_size = os.path.getsize(save_path)
#         return jsonify({
#             'success': True,
#             'filename': filename,
#             'content_type': file.content_type,
#             'size': file_size
#         })
#     return jsonify({'success': False, 'error': 'Invalid file type'}), 400

# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os
from datetime import datetime
import time
from werkzeug.utils import secure_filename

# Load env variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__, static_folder='static', template_folder='templates')

# === Upload support ===
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'webm', 'wav', 'mp3', 'ogg', 'm4a'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

# === Static uploads serving (optional, for debug) ===
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ---------------------------------------------------
# --- Keep the rest of your TTS endpoints as is  ---
# (Omitted in this code block for brevity, but leave your
#  existing /tts, /health, etc. code unchanged.)
# ---------------------------------------------------
# Insert your Murf TTS routes here ...
# (cut for brevity; see your original code or use my previous answer)
# ---------------------------------------------------

# Home page (renders index.html)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host=host, port=port, debug=debug)
