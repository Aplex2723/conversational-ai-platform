from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException
import os
from uuid import uuid4
from app.database import get_db
from app.models import Document
from app.schemas import DocumentResponse
from sqlalchemy.orm import Session
from app.services.pdf_processor import process_document
from loguru import logger

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post(
    "",
    response_model=DocumentResponse,
    summary="Upload and process a PDF document",
    description=(
        "Uploads a PDF file, stores it, and initiates a processing pipeline. "
        "This pipeline extracts the PDF pages, chunks content, obtains embeddings, "
        "and stores vector data in ChromaDB for RAG."
    ),
    responses={
        200: {
            "description": "Successfully uploaded and processed the document. Returns processed document info."
        },
        400: {"description": "Invalid file or data provided."},
        500: {"description": "Internal server error during file handling or processing."}
    }
)
@logger.catch
def upload_document(
    title: str = Form(..., description="Title of the document being uploaded"),
    file: UploadFile = File(..., description="PDF file to be uploaded"),
    db: Session = Depends(get_db)
) -> DocumentResponse:
    """
    Endpoint: **Upload Document**

    - **Form Data**:
        - `title`: A string representing the document's title.
        - `file`: The PDF file upload.
    - **Response**: `DocumentResponse` with the document’s metadata.

    **Processing Steps**:
    1. Validate and save the uploaded PDF file.
    2. Create a `Document` record in the database.
    3. Call `process_document` to:
       - Extract pages
       - Chunk text
       - Embed with OpenAI embeddings
       - Store vectors in ChromaDB
    4. Mark document as processed

    **Constraints**:
    - Only PDF files are supported.
    - Large PDF files might require more time to process.
    """
    logger.info(f"Received document upload request: Title='{title}', Filename='{file.filename}'")
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        logger.error("Uploaded file is not a PDF.")
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Save file locally
    file_id = str(uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    upload_dir = "./uploaded_docs"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{file_id}{file_ext}")
    try:
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        logger.info(f"Saved uploaded file to {file_path}")
    except Exception as e:
        logger.exception(f"Failed to save uploaded file: {e}")
        raise HTTPException(status_code=500, detail="Failed to save the uploaded file.")

    # Create Document record
    try:
        doc = Document(title=title, file_path=file_path, is_processed=False)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        logger.debug(f"Created Document record with ID: {doc.id}")
    except Exception as e:
        logger.exception("Failed to create Document record in database.")
        raise HTTPException(status_code=500, detail="Failed to create Document record.")

    # Process the document
    try:
        process_document(db, doc)
        logger.info(f"Processed document ID: {doc.id} successfully.")
    except Exception as e:
        logger.exception(f"Failed to process document ID: {doc.id}.")
        raise HTTPException(status_code=500, detail="Failed to process the document.")

    return DocumentResponse(
        id=doc.id,
        title=doc.title,
        file_path=doc.file_path,
        is_processed=doc.is_processed
    )