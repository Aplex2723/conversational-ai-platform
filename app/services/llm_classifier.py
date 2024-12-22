from loguru import logger
import openai
from app.config import settings

# Initialize the OpenAI client
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def classify_message(content: str) -> str:
    """
    Classify the message as 'food' or 'weather' using an LLM.
    """
    messages = [
        {"role": "system", "content": "You are a classifier that categorizes user queries into 'food' or 'weather' or 'other' just return one of those words depending on what user wants."},
        {"role": "user", "content": content}
    ]
    logger.info(f"Classifying message: {content}")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=5,
            temperature=0
        )
        classification = response.choices[0].message.content.lower()
        logger.info(f"Message classified as: {classification}")
        if classification not in ["food", "weather", "other"]:
            logger.warning(f"Unexpected classification '{classification}'. Falling back to 'food'.")
            classification = "food"  # fallback
        return classification
    except Exception as e:
        logger.exception("Classification failed. Falling back to 'food'.")
        return "food"  # fallback