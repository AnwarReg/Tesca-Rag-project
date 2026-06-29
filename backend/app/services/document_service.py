import uuid
from io import BytesIO

from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.models import Chunk, Document
from app.services import gemini, storage

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def _extract_text(data: bytes) -> str:
    reader = PdfReader(BytesIO(data))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _chunk(text: str) -> list[str]:
    """Slice text into overlapping fixed-size windows.

    Each window is CHUNK_SIZE chars; we advance by (CHUNK_SIZE - CHUNK_OVERLAP)
    so consecutive windows share CHUNK_OVERLAP chars and no sentence is lost at
    a boundary. Blank/whitespace-only windows are dropped.
    """
    step = CHUNK_SIZE - CHUNK_OVERLAP
    chunks = []
    for start in range(0, len(text), step):
        window = text[start : start + CHUNK_SIZE]
        if window.strip():
            chunks.append(window)
    return chunks


def process_document(
    db: Session, user_id: str, filename: str, data: bytes
) -> Document:
    """Run the full ingest pipeline and persist the document with its chunks."""
    text = _extract_text(data)
    chunks = _chunk(text)
    if not chunks:
        raise ValueError("No extractable text found in the document")

    embeddings = gemini.embed(chunks)

    s3_key = f"{user_id}/{uuid.uuid4()}/{filename}"
    storage.upload(s3_key, data)

    document = Document(clerk_user_id=user_id, filename=filename, s3_key=s3_key)
    document.chunks = [
        Chunk(content=content, embedding=embedding)
        for content, embedding in zip(chunks, embeddings)
    ]
    db.add(document)
    db.commit()
    db.refresh(document)
    return document
