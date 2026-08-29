import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Defina GEMINI_API_KEY no arquivo .env")

GEN_MODEL = os.getenv("GEN_MODEL", "gemini-3.6-flash")
EMBED_MODEL = "gemini-embedding-001"

DB_PATH = os.getenv("DB_PATH", "assistant.db")

client = genai.Client(api_key=GEMINI_API_KEY)