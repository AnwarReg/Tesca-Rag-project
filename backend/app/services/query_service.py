from sqlalchemy.orm import Session

from app.models import Chunk, Document
from app.services import gemini

TOP_K = 5

PROMPT_TEMPLATE = """You are a technical documentation assistant for factory \
technicians. Answer the question using ONLY the context below. If the answer is \
not in the context, say you don't have enough information — do not guess.

Context:
{context}

Question: {question}
"""


def answer_question(
    db: Session, user_id: str, question: str
) -> tuple[str, list[str]]:
    """Retrieve the most relevant chunks for this user and have Gemini answer."""
    query_embedding = gemini.embed([question])[0]

    # Join chunks to their document so we can scope to this user only — a user
    # can never retrieve another tenant's chunks. Order by cosine distance so
    # the closest (most similar) chunks come first.
    chunks = (
        db.query(Chunk)
        .join(Document)
        .filter(Document.clerk_user_id == user_id)
        .order_by(Chunk.embedding.cosine_distance(query_embedding))
        .limit(TOP_K)
        .all()
    )
    if not chunks:
        return "I don't have any documents to answer from yet.", []

    context = "\n\n".join(chunk.content for chunk in chunks)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)
    answer = gemini.generate(prompt)

    sources = sorted({chunk.document.filename for chunk in chunks})
    return answer, sources
