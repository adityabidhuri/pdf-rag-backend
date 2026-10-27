from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from database import db_dependency
from models import Document, User
from schemas import DocumentResponse
from auth import get_current_user

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    db:db_dependency,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed",
        )

    file_path = UPLOAD_DIR / Path(file.filename).name

    file_size = 0

    try:
        with file_path.open("wb") as destination:
            while chunk := await file.read(1024 * 1024):
                file_size += len(chunk)

                if file_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="File size exceeds 10 MB limit",
                    )

                destination.write(chunk)

        new_document = Document(
            filename=Path(file.filename).name,
            file_path=str(file_path),
            owner_id=current_user.id,
        )

        db.add(new_document)
        db.commit()
        db.refresh(new_document)

        return new_document

    except Exception:
        if file_path.exists():
            file_path.unlink()
        raise

    finally:
        await file.close()



@router.get("/", response_model=list[DocumentResponse])
def list_documents(
    db: db_dependency,
    current_user: User = Depends(get_current_user),
):
    documents = (
        db.query(Document)
        .filter(Document.owner_id == current_user.id)
        .order_by(Document.created_at.desc())
        .all()
    )

    return documents



@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: db_dependency,
    current_user: User = Depends(get_current_user),
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.owner_id == current_user.id,
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return document




@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: db_dependency,
    current_user: User = Depends(get_current_user),
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.owner_id == current_user.id,
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    file_path = Path(document.file_path)

    if file_path.exists():
        file_path.unlink()

    db.delete(document)
    db.commit()

    return {
        "message": "Document deleted successfully",
        "document_id": document_id,
    }
