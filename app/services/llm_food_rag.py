from .embeddings import embed_text
from .vector_store import query_vectors
from loguru import logger
from groq import Groq
from app.config import settings

client = Groq(
    api_key= settings.GROQ_API_KEY
)

def generate_food_answer(query: str):
    # We can improve RAG using Hybrid search.
    # 1. Embed query
    query_embedding = embed_text(query)
    logger.info("Query embedded successfully.")
    # 2. Retrieve similar docs
    results = query_vectors(query_embedding)
    logger.info("Retrieved vectors for RAG.")
    # Extract top chunks as context
    context_chunks = []

    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        context_chunks.append(meta['chunk_text'])

    context_text = "\n\n".join(context_chunks)
    logger.info(f"Context for RAG: {context_text[:100]}...")  # Log first 100 chars
    prompt ={
            "role": "system",
            "content": f"You are a helpful food assistant. Use the following context to answer the user:\n\n{context_text}\n\nif the context is not correct, apologize and say that you do not have a recipe.\n\nUser: {query}\n",
        } 

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[prompt],
            temperature=1,
            max_tokens=1024,
            top_p=1,
        )
        answer = completion.choices[0].message.content
        logger.info("Generated food answer using RAG.")
        return answer
    except Exception as e:
        logger.exception("Food LLM call failed.")
        return "I'm sorry, I cannot answer right now."