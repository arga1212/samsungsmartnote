import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Flask server URL
FLASK_SERVER_URL = os.getenv("FLASK_SERVER_URL", "http://localhost:5000")

# Gemini model configuration
GEMINI_MODEL = "gemini-2.0-flash-thinking-exp-01-21"
GEMINI_CONFIG_SUMMARY = {
    'temperature': 0.0,
    'top_p': 1.0,
    'top_k': 0
}

GEMINI_CONFIG_TRANSCRIBE = {
    'temperature': 0.0,
    'top_p': 1.0,
    'top_k': 0
}

GEMINI_CONFIG_MODULE = {
    'max_output_tokens': 300000,
    'temperature': 0.2,
    'top_p': 1.0,
    'top_k': 0
}

GEMINI_CONFIG_QUIZ = {
    'temperature': 0.05,
    'max_output_tokens': 100000
}

# File upload settings
ALLOWED_AUDIO_EXTENSIONS = {"wav", "mp3", "m4a", "ogg"}
MAX_UPLOAD_SIZE_MB = 50

# Paths
UPLOAD_FOLDER = "uploads"
TEMP_FOLDER = "temp"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)