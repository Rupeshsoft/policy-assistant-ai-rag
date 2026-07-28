from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.document import Document

from app.services.document_reader import DocumentReader

router = APIRouter(
    prefix="/reader",
    tags=["Document Reader"]
)


@router.get("/{document_id}")
def read_document(document_id: int,
                  db: Session = Depends(get_db)):

    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    text = DocumentReader.read_document(
        document.filepath
    )

    return {

        "document_id": document.id,

        "filename": document.original_filename,

        "characters": len(text),

        "text": text

    }