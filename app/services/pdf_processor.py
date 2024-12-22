from app.utils.pdf_utils import extract_pages_from_pdf, chunk_text
from app.services.embeddings import embed_text
from app.services.vector_store import add_vector
from loguru import logger
from app.models import DocumentPage

@logger.catch
def process_document(db, doc):
    logger.info(f"Starting processing of document ID: {doc.id}, Title: {doc.title}")
    try:
        pages = extract_pages_from_pdf(doc.file_path)
        logger.info(f"Extracted {len(pages)} pages from PDF.")
        
        for page_number, content in pages:
            logger.debug(f"Processing page {page_number}.")
            # Store DocumentPage in DB
            page_obj = DocumentPage(document_id=doc.id, page_number=page_number, content=content)
            db.add(page_obj)
            db.commit()
            db.refresh(page_obj)
            logger.debug(f"Stored DocumentPage ID: {page_obj.id} in database.")

            # Chunk content
            chunks = chunk_text(content)
            logger.debug(f"Chunked page {page_number} into {len(chunks)} chunks.")

            for i, chunk in enumerate(chunks):
                emb = embed_text(chunk)
                metadata = {
                    "document_id": doc.id,
                    "page_number": page_number,
                    "chunk_id": i,
                    "title": doc.title,
                    "chunk_text": chunk
                }
                vector_id = f"doc{doc.id}_p{page_number}_c{i}"
                add_vector(vector_id, emb, metadata)
                logger.debug(f"Added vector ID: {vector_id} to ChromaDB.")

        doc.is_processed = True
        db.commit()
        logger.info(f"Document ID: {doc.id} processed successfully.")
    except Exception as e:
        logger.exception(f"Failed to process document ID: {doc.id}.")
        raise