# client/config.py

import os
from dotenv import load_dotenv

load_dotenv()

# Server URL
SERVER_URL = os.getenv("SERVER_URL", "http://127.0.0.1:5000/requests")

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if GEMINI_API_KEY is set (only warn, don't raise exception immediately)
def check_api_key():
    """Check if API key is available and raise error if needed"""
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is not set in the environment variables. "
            "Please set it in your .env file or environment. "
            "See .env.example for template."
        )
    return True