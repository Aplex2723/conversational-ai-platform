from .embeddings import embed_text
from .vector_store import query_vectors
from loguru import logger
from groq import Groq
from app.config import settings

client = Groq(
    api_key= settings.GROQ_API_KEY
)

def generate_ooc_answer(query: str):
    logger.info("handling out of classification query.")

    agent_messages = [{
                "role": "system",
                "content": f"You are a helpful assistant. Please advise and apologize to the user as you can only answer questions about the weather in NY or about food.",
            }, 
            {
                "role": "user",
                "content": query
            }
        ]

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=agent_messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
        )
        answer = completion.choices[0].message.content
        logger.info("Generated ooc answer .")
        return answer
    except Exception as e:
        logger.exception("Food LLM call failed.")
        return "I'm sorry, I cannot answer right now."