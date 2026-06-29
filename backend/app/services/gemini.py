from google import genai

from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

EMBEDDING_MODEL = "text-embedding-004"
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
