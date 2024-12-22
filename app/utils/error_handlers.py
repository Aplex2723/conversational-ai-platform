from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger

@logger.catch
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.detail} | Path: {request.url.path} | Method: {request.method}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@logger.catch
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc} | Path: {request.url.path} | Method: {request.method}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."},
    )