import openai
from app.config import settings
from loguru import logger

# Initialize the OpenAI client
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def embed_text(text: str):
    """
    Generate embeddings for the given text using OpenAI's embedding API.
    """
    logger.debug("Generating embedding for text.")
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"  
        )
        logger.debug("Embedding generated successfully.")
        return response.data[0].embedding
    except Exception as e:
        logger.exception(f"Embedding failed: {e}")
        raise