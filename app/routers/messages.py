from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import MessageCreate, MessageResponse
from app.models import Message
from app.services.llm_classifier import classify_message
from app.services.llm_food_rag import generate_food_answer
from app.services.llm_weather import generate_weather_answer
from app.services.llm_ooc import generate_ooc_answer
from app.services.weather_service import get_weather_for_newyork
from loguru import logger

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post(
    "",
    response_model=MessageResponse,
    summary="Create a new user message",
    description=(
        "Stores a user-provided message, classifies it (food or weather), "
        "generates an appropriate AI response, and returns the AI message. "
        "Food queries use RAG with llama-3.3-70b. Weather queries use the OpenWeather API "
        "and GPT-4o for summarization."
    ),
    responses={
        200: {
            "description": "Successfully created and processed the message. Returns the AI-generated message."
        },
        400: {"description": "Invalid input data."},
        500: {"description": "Internal server error."}
    }
)
def create_message(
    msg_in: MessageCreate,
    db: Session = Depends(get_db)
) -> MessageResponse:
    """
    Endpoint: **Create Message**

    - **Request Body**: `MessageCreate` with user content.
    - **Response**: `MessageResponse` representing the newly created AI response.
    
    This endpoint handles:
    1. **Storing the user message** in the database.
    2. **Classification** of the user content (food vs. weather).
    3. **Food Query**: Retrieval-Augmented Generation (RAG) with llama-3.3-70b on Groq.
    4. **Weather Query**: Fetch OpenWeather data for New York, summarized by GPT-4o.
    5. **AI Response** is stored and returned.
    """
    logger.info("Received new message request.")
    try:
        # Store user message
        user_msg = Message(is_ai=False, content=msg_in.content)
        db.add(user_msg)
        db.commit()
        db.refresh(user_msg)
        logger.info(f"Stored user message with ID: {user_msg.id}")

        # Classify the message
        classification = classify_message(user_msg.content)
        logger.info(f"Message classified as: {classification}")

        # Generate response based on classification
        if classification == "food":
            logger.info("Generating response for food query.")
            answer = generate_food_answer(user_msg.content)
        elif classification == "other":
            logger.info("Generating response for out-of-classification query.")
            answer = generate_ooc_answer(user_msg.content)
        else:  # weather
            logger.info("Generating response for weather query.")
            weather_data = get_weather_for_newyork()
            if not weather_data:
                logger.warning("Weather data is empty.")
                answer = "I'm sorry, I can't fetch the weather right now."
            else:
                answer = generate_weather_answer(weather_data)

        # Store AI response
        ai_msg = Message(is_ai=True, content=answer)
        db.add(ai_msg)
        db.commit()
        db.refresh(ai_msg)
        logger.info(f"Stored AI response with ID: {ai_msg.id}")

        logger.info("Responding to message request successfully.")
        return MessageResponse(
            id=ai_msg.id,
            is_ai=ai_msg.is_ai,
            content=ai_msg.content,
            timestamp=ai_msg.timestamp
        )
    except Exception as e:
        logger.exception("Failed to handle message request.")
        raise HTTPException(status_code=500, detail="Internal server error.")