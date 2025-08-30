# app/config/settings.py

import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the root directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- API Keys ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- Application Settings ---
# In a real app, you might have more configs like database URLs, etc.
# For now, we just need the API key.

# --- Validation ---
if not GROQ_API_KEY:
    raise ValueError("🚨 GROQ_API_KEY is not set in the .env file. Please add it.")

