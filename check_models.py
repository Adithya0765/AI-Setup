"""Check available Gemini models"""

import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("NEXUS_PRIMARY_KEYS", "").split(",")[0]

if not api_key or api_key == "your-gemini-key-1":
    print("❌ No API key found in .env")
    print("Please add your Gemini API key to .env file")
    exit(1)

genai.configure(api_key=api_key)

print("Available Gemini models:")
print()

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✓ {model.name}")
        print(f"  Display name: {model.display_name}")
        print()
