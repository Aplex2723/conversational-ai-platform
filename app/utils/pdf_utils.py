import pdfplumber
from loguru import logger

@logger.catch
def extract_pages_from_pdf(file_path: str):
    logger.info(f"Extracting pages from PDF: {file_path}")
    pages_content = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                pages_content.append((i+1, text))
                logger.debug(f"Extracted text from page {i+1}.")
    except Exception as e:
        logger.exception(f"Error reading PDF {file_path}: {e}")
        raise
    logger.info(f"Extracted {len(pages_content)} pages from PDF.")
    return pages_content

@logger.catch
def chunk_text(text: str, max_length: int = 1000):
    logger.debug("Starting text chunking.")
    chunks = []
    words = text.split()
    current_chunk = []
    length = 0
    for w in words:
        if length + len(w) + 1 <= max_length:
            current_chunk.append(w)
            length += len(w) + 1
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [w]
            length = len(w) + 1
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    logger.debug(f"Text chunked into {len(chunks)} chunks.")
    return chunks