from google import genai

from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

EMBEDDING_MODEL = "text-embedding-004"
GENERATION_MODEL = "gemini-2.0-flash"
# text-embedding-004 caps how many texts one call may embed, so we chunk the
# list into batches and stitch the results back together.
EMBED_BATCH = 100


def embed(texts: list[str]) -> list[list[float]]:
    """Turn a list of texts into 768-dim embedding vectors, preserving order."""
    vectors: list[list[float]] = []
    for start in range(0, len(texts), EMBED_BATCH):
        batch = texts[start : start + EMBED_BATCH]
        response = client.models.embed_content(model=EMBEDDING_MODEL, contents=batch)
        vectors.extend(item.values for item in response.embeddings)
    return vectors


def generate(prompt: str) -> str:
    """Generate an answer from a fully-built prompt string."""
    response = client.models.generate_content(model=GENERATION_MODEL, contents=prompt)
    return response.text
