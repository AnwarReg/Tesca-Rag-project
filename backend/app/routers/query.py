from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.services.query_service import answer_question

router = APIRouter(prefix="/query", tags=["query"])


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("", response_model=QueryResponse)
def query(
    body: QueryRequest,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    answer, sources = answer_question(db, user_id, body.question)
    return QueryResponse(answer=answer, sources=sources)
