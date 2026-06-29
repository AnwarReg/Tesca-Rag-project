from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.dependencies import get_current_user

router = APIRouter(prefix="/query", tags=["query"])


class QueryRequest(BaseModel):
    question: str


@router.post("")
def query(
    body: QueryRequest,
    user_id: str = Depends(get_current_user),
):
    # Retrieval + Gemini generation is built in Step 3.
    raise HTTPException(
        status.HTTP_501_NOT_IMPLEMENTED, "Query pipeline arrives in step 3"
    )
