from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from loguru import logger

Base = declarative_base()

engine = create_engine(settings.DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

try:
    Base.metadata.create_all(bind=engine, checkfirst=True)
    logger.info("Database tables ensured.")
except Exception as e:
    logger.exception("Failed to ensure database tables exist.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()