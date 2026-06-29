from fastapi import FastAPI

from app.routers import documents, query

app = FastAPI(title="Tesca RAG API")

app.include_router(documents.router)
app.include_router(query.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
