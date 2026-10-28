from embedding_service import client
from google.genai import types

print("Testing Gemini connection...", flush=True)

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Reply with exactly: Gemini is working.",
        config=types.GenerateContentConfig(
            http_options=types.HttpOptions(
                timeout=15000,
                retry_options=types.HttpRetryOptions(
                    attempts=1,
                ),
            ),
        ),
    )

    print("Response received:", response.text, flush=True)

except Exception as error:
    print("Gemini request failed:", repr(error), flush=True)