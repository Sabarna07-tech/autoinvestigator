import google.generativeai as genai
from shared.config import GEMINI_KEY, GEMINI_MODEL
import os

class GeminiAgent(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GeminiAgent, cls).__new__(cls)
        return cls.instance
        
    def __init__(self):
        # This check prevents re-initialization in the singleton pattern
        if not hasattr(self, 'model'):
            try:
                # Use os.getenv directly as it's more standard than importing a variable
                api_key = os.getenv('GEMINI_API_KEY') 
                if not api_key:
                    raise ValueError("GEMINI_API_KEY environment variable not set.")
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel(GEMINI_MODEL)
                print("[GeminiAgent] Initialized successfully.")
            except Exception as e:
                print(f"[GeminiAgent] Error during initialization: {e}")
                self.model = None
            
    def run(self, query:str) -> str: # <--- RENAMED from execute to run
        """
        Generates content using the Gemini model.
        """
        if not self.model:
            return "Error: Gemini Agent not initialized correctly."

        try:
            print(f"[GeminiAgent] Generating content...")
            response = self.model.generate_content(query)
            return response.text
        except Exception as e:
            print(f"[GeminiAgent] An error occurred while generating content: {e}")
            return f"Error from Gemini API: {e}"