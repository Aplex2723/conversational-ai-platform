from fastapi import FastAPI
from app.routers import messages, documents
from app.utils.error_handlers import http_exception_handler, general_exception_handler
from fastapi.exceptions import HTTPException
from app.logging_config import logger

def create_app():
    app = FastAPI(title="Conversational AI Platform", version="1.0")

    # Include routers
    app.include_router(messages.router)
    app.include_router(documents.router)

    # Exception handlers
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI application with Uvicorn.")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)