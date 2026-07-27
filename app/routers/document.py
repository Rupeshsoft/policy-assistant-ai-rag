from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Form
from fastapi import Request

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.document import Document

from app.auth.security import get_current_user, _validate_token_and_get_user, oauth2_scheme

from fastapi.responses import FileResponse

from app.services.file_service import save_file

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


async def _resolve_upload_user(
    request: Request,
    bearer_token: str | None = Depends(oauth2_scheme),
    token: str | None = Form(None),
    db: Session = Depends(get_db)
):
    """
    Resolve the current user for the upload endpoint using:
    1. Authorization header (Bearer token)
    2. Explicit 'token' form field
    3. 'token' query parameter
    """
    # Method 1: Bearer token from Authorization header
    if bearer_token:
        return _validate_token_and_get_user(bearer_token, db)

    # Method 2: Explicit form field 'token'
    if token:
        return _validate_token_and_get_user(token, db)

    # Method 3: Query parameter 'token'
    query_token = request.query_params.get("token")
    if query_token:
        return _validate_token_and_get_user(query_token, db)

    raise HTTPException(
        status_code=401,
        detail="Not authenticated. Provide Authorization header, or 'token' form/query parameter."
    )


@router.post("/upload")
async def upload_document(

        file: UploadFile = File(...),

        current_user=Depends(_resolve_upload_user),

        db: Session = Depends(get_db)

):

    try:

        saved = await save_file(file)

        document = Document(

            filename=saved["filename"],

            original_filename=file.filename,

            filepath=saved["filepath"],

            filetype=saved["extension"],

            filesize=saved["filesize"],

            uploaded_by=current_user.id

        )

        db.add(document)

        db.commit()

        db.refresh(document)

        return {

            "message": "Upload Successful",

            "document_id": document.id

        }

    except Exception as e:

        raise HTTPException(400, str(e))
    
    
    
    
@router.get("/")
def list_documents(

        db: Session = Depends(get_db),

        current_user=Depends(get_current_user)

):

    docs = db.query(Document).filter(

        Document.uploaded_by == current_user.id

    ).all()

    return docs


@router.get("/{document_id}")
def get_document(

        document_id: int,

        db: Session = Depends(get_db),

        current_user=Depends(get_current_user)

):

    doc = db.query(Document).filter(

        Document.id == document_id,

        Document.uploaded_by == current_user.id

    ).first()

    if not doc:
        raise HTTPException(404, "Document not found")

    return doc





@router.get("/download/{document_id}")
def download(

        document_id: int,

        db: Session = Depends(get_db),

        current_user=Depends(get_current_user)

):

    doc = db.query(Document).filter(

        Document.id == document_id,

        Document.uploaded_by == current_user.id

    ).first()

    if not doc:
        raise HTTPException(404, "Document not found")

    return FileResponse(
        path=doc.filepath,
        filename=doc.original_filename
    )
    
    
    
import os


@router.delete("/{document_id}")
def delete_document(

        document_id: int,

        db: Session = Depends(get_db),

        current_user=Depends(get_current_user)

):

    doc = db.query(Document).filter(

        Document.id == document_id,

        Document.uploaded_by == current_user.id

    ).first()

    if not doc:
        raise HTTPException(404, "Document not found")

    if os.path.exists(doc.filepath):
        os.remove(doc.filepath)

    db.delete(doc)

    db.commit()

    return {

        "message": "Deleted Successfully"
    }    