from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Document

router = APIRouter(prefix="/documents", tags=["documents"])


class DocumentOut(BaseModel):
    id: int
    filename: str
    created_at: datetime

    # Lets Pydantic read straight from a SQLAlchemy model instance.
    model_config = ConfigDict(from_attributes=True)


@router.get("", response_model=list[DocumentOut])
def list_documents(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Document)
        .filter(Document.clerk_user_id == user_id)
        .order_by(Document.created_at.desc())
        .all()
    )


@router.post("", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # The parse -> chunk -> embed -> store pipeline is built in Step 2.
    raise HTTPException(
        status.HTTP_501_NOT_IMPLEMENTED, "Document processing arrives in step 2"
    )
