import os
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Defina GROQ_API_KEY no arquivo .env")

GEN_MODEL = os.getenv("GEN_MODEL", "openai/gpt-oss-20b")
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

DB_PATH = os.getenv("DB_PATH", "assistant.db")

client = Groq(api_key=GROQ_API_KEY)

# Carrega o modelo de embedding uma unica vez (roda localmente, sem API externa)
embedding_model = SentenceTransformer(EMBED_MODEL_NAME)