# client/config.py

import os
from dotenv import load_dotenv

load_dotenv()

# Server URL
SERVER_URL = os.getenv("SERVER_URL", "http://127.0.0.1:8000/requests")

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if GEMINI_API_KEY is set
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
