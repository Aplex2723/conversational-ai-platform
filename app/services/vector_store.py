import chromadb
from chromadb.config import Settings
from loguru import logger

client = chromadb.PersistentClient(path="./.chromadb")
collection = client.get_or_create_collection(name="documents")
logger.info("ChromaDB collection 'documents' initialized.")

@logger.catch
def add_vector(id: str, embedding: list, metadata: dict):
    logger.info(f"Adding vector with ID: {id} and metadata: {{'document_id': {metadata.get('document_id')}, 'page_number': {metadata.get('page_number')}, 'chunk_id': {metadata.get('chunk_id')}}}")
    try:
        collection.add(ids=[id], embeddings=[embedding], metadatas=[metadata])
        logger.debug(f"Vector {id} added to ChromaDB successfully.")
    except Exception as e:
        logger.exception(f"Failed to add vector {id} to ChromaDB.")
        raise

@logger.catch
def query_vectors(query_embedding: list, top_k: int = 3):
    logger.info("Querying vectors from ChromaDB.")
    try:
        results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
        logger.debug(f"Retrieved {len(results['documents'][0])} vectors from ChromaDB.")
        return results
    except Exception as e:
        logger.exception("Failed to query vectors from ChromaDB.")
        raise