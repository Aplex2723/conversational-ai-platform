from sqlalchemy import Column, Integer, Boolean, Text, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    is_ai = Column(Boolean, default=False, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    is_processed = Column(Boolean, default=False, nullable=False)
    pages = relationship("DocumentPage", back_populates="document")

class DocumentPage(Base):
    __tablename__ = "document_pages"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    is_processed = Column(Boolean, default=False, nullable=False)
    document = relationship("Document", back_populates="pages")