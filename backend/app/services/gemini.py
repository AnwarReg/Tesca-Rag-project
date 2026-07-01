import time

from google import genai
from google.genai import errors, types

from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

EMBEDDING_MODEL = "gemini-embedding-001"
GENERATION_MODEL = "gemini-2.5-flash"
# gemini-embedding-001 defaults to 3072 dims; we request 768 so the vectors
# match our Vector(768) column without a schema change.
EMBED_DIM = 768
# Cap on how many texts one call may embed, so we batch and stitch results.
EMBED_BATCH = 100
# Free-tier embedding quota resets per minute; on a 429 we wait it out and retry.
MAX_RETRIES = 5
RATE_LIMIT_WAIT = 35


def _embed_batch(batch: list[str]) -> list[list[float]]:
    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=batch,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            return [item.values for item in response.embeddings]
        except errors.ClientError as exc:
            # 429 = free-tier rate limit. Wait for the window to reset, then retry.
            if exc.code == 429 and attempt < MAX_RETRIES - 1:
                time.sleep(RATE_LIMIT_WAIT)
                continue
            raise
    raise RuntimeError("Embedding failed after retries")


def embed(texts: list[str]) -> list[list[float]]:
    """Turn a list of texts into 768-dim embedding vectors, preserving order."""
    vectors: list[list[float]] = []
    for start in range(0, len(texts), EMBED_BATCH):
        vectors.extend(_embed_batch(texts[start : start + EMBED_BATCH]))
    return vectors


def generate(prompt: str) -> str:
    """Generate an answer from a fully-built prompt string."""
    response = client.models.generate_content(model=GENERATION_MODEL, contents=prompt)
    return response.text
