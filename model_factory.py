# model_factory.py
import google.generativeai as genai
import os

class ModelFactory:
    def __init__(self, api_key=None, model_name="gemini-2.0-flash"):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY") or "........"
        if not api_key:
            raise ValueError("API key not provided and GEMINI_API_KEY env variable is not set.")
        genai.configure(api_key=api_key)
        self.model_name = model_name

    def get_chat_model(self):
        return genai.GenerativeModel(model_name=self.model_name)
