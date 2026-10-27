
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )

client = genai.Client(api_key=api_key)

EMBEDDING_MODEL = "gemini-embedding-2"


def embed_text(text: str) -> list[float]:
    if not text.strip():
        raise ValueError("Cannot generate an embedding for empty text")

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )

    if not result.embeddings:
        raise RuntimeError("The embedding API returned no embeddings")

    return result.embeddings[0].values
